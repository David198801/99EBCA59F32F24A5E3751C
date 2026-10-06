#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import struct
import traceback

try:
    import olefile
except ImportError:
    print("缺少依赖：olefile")
    print("请执行：pip install olefile")
    sys.exit(1)

try:
    import xlrd
except ImportError:
    xlrd = None


OLE_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")
ZIP_MAGIC = bytes.fromhex("504B0304")
XML_MAGIC = b"<?xml"
HTML_MAGIC_PREFIXES = [
    b"<html",
    b"<!doc",
    b"<table",
]


RECORD_NAMES = {
    0x0809: "BOF",
    0x000A: "EOF",
    0x002F: "FilePass",
    0x0042: "CodePage",
    0x0085: "BoundSheet",
    0x00FC: "SST",
    0x003C: "Continue",
    0x0006: "Formula",
    0x0203: "Number",
    0x00FD: "LabelSST",
    0x0201: "Blank",
    0x0204: "Label",
    0x027E: "RK",
    0x00E0: "XF",
    0x0031: "Font",
    0x00E5: "MergeCells",
}


BOF_TYPES = {
    0x0005: "Workbook Globals",
    0x0010: "Worksheet",
    0x0020: "Chart",
    0x0040: "Macro Sheet",
    0x0006: "VB Module",
}


def hex4(n):
    return f"0x{n:04X}"


def print_section(title):
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def detect_file_type(path):
    with open(path, "rb") as f:
        head = f.read(512)

    if head.startswith(OLE_MAGIC):
        return "OLE2/XLS", "文件头是 OLE2，符合传统 .xls 容器格式"

    if head.startswith(ZIP_MAGIC):
        return "ZIP/XLSX", "文件实际像是 .xlsx/.xlsm，而不是 .xls"

    stripped = head.lstrip().lower()

    if stripped.startswith(XML_MAGIC):
        return "XML", "文件实际像是 XML Spreadsheet 2003，而不是二进制 .xls"

    for prefix in HTML_MAGIC_PREFIXES:
        if stripped.startswith(prefix):
            return "HTML", "文件实际像是 HTML 表格伪装成 .xls"

    if b"<html" in stripped[:200] or b"<table" in stripped[:200]:
        return "HTML", "文件内容包含 HTML 标记，可能是 HTML 伪装成 .xls"

    return "UNKNOWN", "文件头不是标准 OLE2，也不像 xlsx/html/xml"


def list_ole_entries(ole):
    print_section("OLE 目录结构")

    for entry in ole.listdir(streams=True, storages=True):
        print("/".join(entry))


def find_workbook_stream(ole):
    candidates = [
        ["Workbook"],
        ["Book"],
        ["WORKBOOK"],
        ["BOOK"],
    ]

    for c in candidates:
        if ole.exists(c):
            return c

    return None


def read_stream(ole, stream_path):
    with ole.openstream(stream_path) as s:
        return s.read()


def parse_biff_records(data):
    """
    返回：
    records: list of dict
    errors: list[str]
    warnings: list[str]
    """
    records = []
    errors = []
    warnings = []

    pos = 0
    index = 0
    eof_depth = 0
    bof_count = 0
    eof_count = 0
    filepass_found = False
    boundsheets = []

    data_len = len(data)

    while pos < data_len:
        if pos + 4 > data_len:
            errors.append(
                f"位置 {pos} 处不足 4 字节，无法读取 BIFF 记录头，文件可能被截断"
            )
            break

        sid, length = struct.unpack_from("<HH", data, pos)
        payload_start = pos + 4
        payload_end = payload_start + length

        name = RECORD_NAMES.get(sid, "Unknown")

        if payload_end > data_len:
            errors.append(
                f"记录 #{index} {hex4(sid)} {name} 在位置 {pos} 声明长度 {length}，"
                f"但超出 Workbook 流大小 {data_len}，文件可能损坏或截断"
            )
            break

        payload = data[payload_start:payload_end]

        record = {
            "index": index,
            "pos": pos,
            "sid": sid,
            "name": name,
            "length": length,
        }
        records.append(record)

        if sid == 0x0809:  # BOF
            bof_count += 1
            eof_depth += 1

            if length >= 8:
                version, bof_type = struct.unpack_from("<HH", payload, 0)
                bof_type_name = BOF_TYPES.get(bof_type, "Unknown")
                record["bof_version"] = version
                record["bof_type"] = bof_type
                record["bof_type_name"] = bof_type_name

                if version not in (0x0600, 0x0500, 0x0000, 0x0007, 0x0200, 0x0300, 0x0400):
                    warnings.append(
                        f"位置 {pos} 的 BOF 版本异常：{hex4(version)}"
                    )

            else:
                warnings.append(f"位置 {pos} 的 BOF 记录长度过短：{length}")

        elif sid == 0x000A:  # EOF
            eof_count += 1
            eof_depth -= 1

            if eof_depth < 0:
                warnings.append(
                    f"位置 {pos} 出现 EOF，但此前没有匹配的 BOF"
                )
                eof_depth = 0

        elif sid == 0x002F:  # FilePass
            filepass_found = True
            warnings.append(
                f"发现 FilePass 加密记录，位置 {pos}。该 xls 可能被加密或使用了特殊保护。"
            )

        elif sid == 0x0085:  # BoundSheet
            if length >= 8:
                lbPlyPos = struct.unpack_from("<I", payload, 0)[0]
                sheet_state = payload[4]
                sheet_type = payload[5]
                name_len = payload[6]
                name_flag = payload[7]

                boundsheets.append({
                    "record_pos": pos,
                    "sheet_offset": lbPlyPos,
                    "sheet_state": sheet_state,
                    "sheet_type": sheet_type,
                    "name_len": name_len,
                    "name_flag": name_flag,
                })

                if lbPlyPos >= data_len:
                    errors.append(
                        f"BoundSheet 位置 {pos} 指向的 Sheet 偏移 {lbPlyPos} 超出 Workbook 流大小 {data_len}"
                    )
            else:
                errors.append(
                    f"BoundSheet 记录位置 {pos} 长度过短：{length}"
                )

        if length > 8224:
            warnings.append(
                f"记录 #{index} {hex4(sid)} {name} 在位置 {pos} 长度 {length} 超过 BIFF8 常见最大记录长度 8224"
            )

        pos = payload_end
        index += 1

    if pos != data_len:
        warnings.append(
            f"BIFF 解析结束位置 {pos} 与 Workbook 流大小 {data_len} 不一致"
        )

    if bof_count == 0:
        errors.append("没有找到 BOF 记录，Workbook 流不像有效 BIFF 数据")

    if eof_depth != 0:
        warnings.append(
            f"BOF/EOF 不完全匹配，未闭合层级：{eof_depth}，BOF 数：{bof_count}，EOF 数：{eof_count}"
        )

    return records, boundsheets, errors, warnings, filepass_found


def check_boundsheet_offsets(data, boundsheets):
    errors = []
    warnings = []

    for i, bs in enumerate(boundsheets):
        offset = bs["sheet_offset"]

        if offset + 4 > len(data):
            errors.append(
                f"第 {i + 1} 个 BoundSheet 指向偏移 {offset}，无法读取 BOF 头"
            )
            continue

        sid, length = struct.unpack_from("<HH", data, offset)

        if sid != 0x0809:
            errors.append(
                f"第 {i + 1} 个 BoundSheet 指向偏移 {offset}，但该位置不是 BOF，实际记录 ID 为 {hex4(sid)}"
            )
        else:
            if length < 8:
                warnings.append(
                    f"第 {i + 1} 个 Sheet 偏移 {offset} 处 BOF 长度过短：{length}"
                )
            else:
                payload = data[offset + 4: offset + 4 + length]
                version, bof_type = struct.unpack_from("<HH", payload, 0)
                bof_type_name = BOF_TYPES.get(bof_type, "Unknown")
                print(
                    f"BoundSheet #{i + 1}: sheet_offset={offset}, "
                    f"BOF version={hex4(version)}, type={hex4(bof_type)} {bof_type_name}"
                )

    return errors, warnings


def summarize_records(records, limit=80):
    print_section("BIFF 记录摘要")

    print(f"记录总数：{len(records)}")
    print()

    print(f"前 {min(limit, len(records))} 条记录：")
    for r in records[:limit]:
        extra = ""
        if r["sid"] == 0x0809:
            extra = f", bof_type={hex4(r.get('bof_type', 0))} {r.get('bof_type_name', '')}"

        print(
            f"#{r['index']:06d} "
            f"pos={r['pos']:10d} "
            f"sid={hex4(r['sid'])} "
            f"{r['name']:12s} "
            f"len={r['length']:5d}"
            f"{extra}"
        )

    if len(records) > limit:
        print(f"... 省略 {len(records) - limit} 条")


def try_xlrd(path):
    print_section("xlrd 打开测试")

    if xlrd is None:
        print("未安装 xlrd，跳过。")
        print("可执行：pip install xlrd==1.2.0")
        return

    try:
        book = xlrd.open_workbook(path, formatting_info=False)
        print("xlrd 可以打开该文件。")
        print(f"Sheet 数量：{book.nsheets}")
        print(f"Sheet 名称：{book.sheet_names()}")
    except Exception as e:
        print("xlrd 打开失败：")
        print(type(e).__name__, str(e))
        print()
        traceback.print_exc()


def main(path):
    print_section("基本信息")

    print(f"文件：{path}")

    if not os.path.exists(path):
        print("文件不存在")
        sys.exit(2)

    size = os.path.getsize(path)
    print(f"大小：{size} bytes")

    file_type, file_type_msg = detect_file_type(path)
    print(f"类型判断：{file_type}")
    print(f"说明：{file_type_msg}")

    if file_type != "OLE2/XLS":
        print()
        print("结论：该文件不是标准二进制 .xls。")
        print("如果 Apache POI 使用 HSSFWorkbook 读取，会很可能失败。")
        print("建议确认文件真实格式，或者用 Excel/WPS 另存为真正的 .xls/.xlsx。")
        return

    print_section("OLE 容器检查")

    if not olefile.isOleFile(path):
        print("olefile 判断该文件不是有效 OLE 文件。")
        print("可能是 OLE 容器损坏。")
        return

    try:
        ole = olefile.OleFileIO(path)
    except Exception as e:
        print("打开 OLE 容器失败：")
        print(type(e).__name__, str(e))
        return

    try:
        print("OLE 容器可以打开。")
        list_ole_entries(ole)

        workbook_stream = find_workbook_stream(ole)

        print_section("Workbook 流检查")

        if workbook_stream is None:
            print("没有找到 Workbook 或 Book 流。")
            print("这通常说明它不是标准 Excel 97-2003 .xls 文件，或 OLE 结构异常。")
            return

        print(f"找到 Workbook 流：{'/'.join(workbook_stream)}")

        try:
            workbook_data = read_stream(ole, workbook_stream)
        except Exception as e:
            print("读取 Workbook 流失败：")
            print(type(e).__name__, str(e))
            return

        print(f"Workbook 流大小：{len(workbook_data)} bytes")

        records, boundsheets, errors, warnings, filepass_found = parse_biff_records(workbook_data)

        summarize_records(records)

        print_section("BoundSheet 偏移检查")

        if not boundsheets:
            print("没有找到 BoundSheet 记录。")
            print("如果这是正常工作簿，通常应该有 BoundSheet。")
        else:
            bs_errors, bs_warnings = check_boundsheet_offsets(workbook_data, boundsheets)
            errors.extend(bs_errors)
            warnings.extend(bs_warnings)

        print_section("问题汇总")

        if errors:
            print("[严重问题]")
            for i, msg in enumerate(errors, 1):
                print(f"{i}. {msg}")
        else:
            print("[严重问题] 未发现")

        print()

        if warnings:
            print("[警告]")
            for i, msg in enumerate(warnings, 1):
                print(f"{i}. {msg}")
        else:
            print("[警告] 未发现")

        print_section("初步结论")

        if errors:
            print("该文件存在明显结构异常，Apache POI 读取失败是合理的。")
            print("常见原因：文件截断、Workbook 流损坏、BoundSheet 偏移错误、BIFF 记录长度异常。")
        elif filepass_found:
            print("文件包含加密记录 FilePass。")
            print("如果没有正确密码，POI/xlrd 可能无法读取。")
        elif warnings:
            print("未发现致命错误，但存在非标准或可疑结构。")
            print("Excel 可能具有更强的容错能力，打开后另存为会重写为规范结构，因此 POI 可以读取。")
        else:
            print("没有发现明显结构问题。")
            print("如果 POI 仍然读取失败，请结合 POI 报错堆栈进一步定位。")

        try_xlrd(path)

    finally:
        ole.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：")
        print("  python check_xls.py your_file.xls")
        sys.exit(1)

    main(sys.argv[1])
