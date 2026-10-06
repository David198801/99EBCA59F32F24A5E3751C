#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import struct
import binascii
import olefile

FONT_SID = 0x0031
BOF_SID = 0x0809
EOF_SID = 0x000A

OLE_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")


def hex4(n):
    return f"0x{n:04X}"


def hex_bytes(b):
    return binascii.hexlify(b).decode("ascii").upper()


def find_workbook_stream(ole):
    for name in (["Workbook"], ["Book"], ["WORKBOOK"], ["BOOK"]):
        if ole.exists(name):
            return name
    return None


def parse_unicode_string_no_len(data, offset, char_count, is_16bit):
    """
    BIFF Short XL Unicode String (不带长度字段，长度已由外部给出)
    返回: (text_bytes_consumed, text_preview)
    """
    if is_16bit:
        byte_len = char_count * 2
        raw = data[offset: offset + byte_len]
        try:
            text = raw.decode("utf-16le", errors="replace")
        except Exception:
            text = repr(raw)
        return byte_len, text
    else:
        byte_len = char_count
        raw = data[offset: offset + byte_len]
        try:
            text = raw.decode("latin1", errors="replace")
        except Exception:
            text = repr(raw)
        return byte_len, text


def try_parse_font_record(payload):
    """
    按 BIFF8 FontRecord 常见结构尝试解析：
    offset  size  field
    0       2     dyHeight
    2       2     grbit
    4       2     icv
    6       2     bls
    8       2     sss
    10      1     uls
    11      1     bFamily
    12      1     bCharSet
    13      1     reserved
    14      1     cch
    15      1     flags
    16      ?     font name

    返回 dict
    """
    result = {
        "ok": False,
        "reason": "",
        "consumed": 0,
        "remaining": 0,
        "fields": {},
    }

    if len(payload) < 16:
        result["reason"] = f"payload 太短，只有 {len(payload)} 字节，连 FontRecord 固定头都不够"
        return result

    dyHeight, grbit, icv, bls, sss = struct.unpack_from("<HHHHH", payload, 0)
    uls = payload[10]
    bFamily = payload[11]
    bCharSet = payload[12]
    reserved = payload[13]
    cch = payload[14]
    flags = payload[15]

    is_16bit = flags & 0x01

    consumed = 16
    name_consumed, name_preview = parse_unicode_string_no_len(payload, consumed, cch, is_16bit)
    consumed += name_consumed

    if consumed > len(payload):
        result["reason"] = (
            f"按 BIFF8 FontRecord 解析时，字体名字需要 {name_consumed} 字节，"
            f"总共要消费 {consumed} 字节，但 payload 实际只有 {len(payload)} 字节"
        )
        return result

    result["ok"] = True
    result["consumed"] = consumed
    result["remaining"] = len(payload) - consumed
    result["fields"] = {
        "dyHeight": dyHeight,
        "grbit": grbit,
        "icv": icv,
        "bls": bls,
        "sss": sss,
        "uls": uls,
        "bFamily": bFamily,
        "bCharSet": bCharSet,
        "reserved": reserved,
        "cch": cch,
        "flags": flags,
        "is_16bit": bool(is_16bit),
        "font_name_preview": name_preview,
    }
    return result


def dump_font_records(workbook_data):
    pos = 0
    idx = 0
    found = 0

    while pos + 4 <= len(workbook_data):
        sid, length = struct.unpack_from("<HH", workbook_data, pos)
        start = pos + 4
        end = start + length

        if end > len(workbook_data):
            print(f"[ERROR] record#{idx} sid={hex4(sid)} 长度越界")
            break

        payload = workbook_data[start:end]

        if sid == FONT_SID:
            found += 1
            print("=" * 100)
            print(f"FontRecord #{found}  at workbook_pos={pos}, payload_len={length}")

            parsed = try_parse_font_record(payload)
            if not parsed["ok"]:
                print(f"  [解析失败] {parsed['reason']}")
            else:
                f = parsed["fields"]
                print(f"  dyHeight   = {f['dyHeight']}")
                print(f"  grbit      = {hex4(f['grbit'])}")
                print(f"  icv        = {f['icv']}")
                print(f"  bls        = {f['bls']}")
                print(f"  sss        = {f['sss']}")
                print(f"  uls        = {f['uls']}")
                print(f"  bFamily    = {f['bFamily']}")
                print(f"  bCharSet   = {f['bCharSet']}")
                print(f"  reserved   = {f['reserved']}")
                print(f"  cch        = {f['cch']}")
                print(f"  flags      = {hex4(f['flags'])}")
                print(f"  is_16bit   = {f['is_16bit']}")
                print(f"  font_name  = {repr(f['font_name_preview'])}")
                print(f"  consumed   = {parsed['consumed']}")
                print(f"  remaining  = {parsed['remaining']}")

                if parsed["remaining"] > 0:
                    tail = payload[parsed["consumed"]:]
                    print(f"  [异常] 记录尾部还有 {parsed['remaining']} 字节未被消费")
                    print(f"  tail_hex   = {hex_bytes(tail)}")

            print(f"  full_hex   = {hex_bytes(payload[:64])}" + ("..." if len(payload) > 64 else ""))

        pos = end
        idx += 1

    if found == 0:
        print("没有找到 FontRecord(0x31)")


def main(path):
    with open(path, "rb") as f:
        head = f.read(8)
    if head != OLE_MAGIC:
        print("不是标准 OLE2 xls")
        return

    if not olefile.isOleFile(path):
        print("不是有效 OLE 文件")
        return

    ole = olefile.OleFileIO(path)
    try:
        wb = find_workbook_stream(ole)
        if not wb:
            print("找不到 Workbook/Book 流")
            return

        with ole.openstream(wb) as s:
            data = s.read()

        dump_font_records(data)
    finally:
        ole.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python check_xls_fontrecord.py xxx.xls")
        sys.exit(1)
    main(sys.argv[1])