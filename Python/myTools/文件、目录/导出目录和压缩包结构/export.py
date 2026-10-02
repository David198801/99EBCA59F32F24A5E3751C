# -*- coding: utf-8 -*-

import os
import re
import sys
import zipfile
import rarfile
import py7zr
import chardet

# --- 配置 ---
# 在此处设置要扫描的根目录路径
# 例如: "D:\\Downloads" 或 "/home/user/documents"
# 如果留空，则从命令行接收第一个参数作为路径
TARGET_PATH = "" 
OUTPUT_FILE = "output.txt"
ERROR_FILE = "output.error.txt"

# --- 全局变量 ---
# 用于存储已经作为分卷一部分处理过的文件，避免重复扫描
processed_volume_parts = set()

def get_rar_volume_parts(filepath, files_in_dir):
    """
    检查filepath是否为RAR分卷的起始文件。
    如果是，返回该分卷的所有文件部分组成的集合。否则返回None。
    """
    filename = os.path.basename(filepath)
    # 新格式: .part01.rar, .part02.rar ...
    part_match = re.match(r'^(.*?)\.part([0-9]+)\.(?:rar|exe)$', filename, re.IGNORECASE)
    if part_match and int(part_match.group(2)) == 1:
        base_name = part_match.group(1)
        pattern = re.compile(f'^{re.escape(base_name)}\.part[0-9]+\.rar$', re.IGNORECASE)
        parts = {f for f in files_in_dir if pattern.match(f)}
        return parts

    # 旧格式: .rar, .r00, .r01 ...
    # 起始文件是 .rar
    if filename.lower().endswith('.rar'):
        base_name = filename[:-4]
        # 检查是否存在 .r00 或 .r01 分卷，这是旧格式分卷的标志
        r_vol_pattern = re.compile(f'^{re.escape(base_name)}\.r[0-9]{2}$', re.IGNORECASE)
        r_vols_exist = any(r_vol_pattern.match(f) for f in files_in_dir)
        if r_vols_exist:
            pattern = re.compile(f'^{re.escape(base_name)}\.(r[0-9]{2}|rar)$', re.IGNORECASE)
            parts = {f for f in files_in_dir if pattern.match(f)}
            return parts
            
    return None

def get_7z_volume_parts(filepath, files_in_dir):
    """
    检查filepath是否为7z分卷的起始文件 (.7z.001)。
    如果是，返回该分卷的所有文件部分组成的集合。否则返回None。
    """
    if filepath.lower().endswith('.7z.001'):
        base_name = os.path.basename(filepath)[:-8] # "archive.7z.001" -> "archive"
        pattern = re.compile(f'^{re.escape(base_name)}\.7z\.[0-9]+$', re.IGNORECASE)
        parts = {f for f in files_in_dir if pattern.match(f)}
        return parts
    return None

def get_zip_volume_parts(filepath, files_in_dir):
    """
    检查filepath是否为Zip分卷的起始文件 (.z01)。
    如果是，返回该分卷的所有文件部分组成的集合。否则返回None。
    """
    if filepath.lower().endswith('.z01'):
        base_name = os.path.basename(filepath)[:-4] # "archive.z01" -> "archive"
        pattern = re.compile(f'^{re.escape(base_name)}\.(z[0-9]{2}|zip)$', re.IGNORECASE)
        parts = {f for f in files_in_dir if pattern.match(f)}
        return parts
    return None

def deal_name_encoding(s,archive_name):
    b = None
    try:
        b = s.encode('cp437')
    except:
        return s
    #识别编码
    c = "gbk"
    if archive_name.upper().startswith("RJ"):#特殊处理，RJ开头的压缩包，识别不到则默认日文
        c = "shift-jis"
    result = chardet.detect(b)
    if result and result["encoding"] and result["confidence"]>0.9:
        c = result["encoding"]
        
    name = b.decode(c, errors='replace')
    return name


def list_archive_files(archive_path):
    """
    列出压缩包内的所有文件路径（对单文件和分卷起始文件都有效）。
    返回一个包含内部文件路径的列表。如果出错，则会抛出异常。
    """
    internal_files = []
    abs_archive_path = os.path.abspath(archive_path)
    
    try:
        # 使用 is_rarfile/is_7zfile 判断更可靠
        if rarfile.is_rarfile(archive_path):
            with rarfile.RarFile(archive_path, 'r', charset='cp437') as rf:
                for item in rf.infolist():
                    if not item.is_dir():
                        filename = deal_name_encoding(item.filename,os.path.basename(archive_path))
                        internal_path = os.path.join(abs_archive_path, filename).replace('\\', '/')
                        internal_files.append(internal_path)
        
        elif py7zr.is_7zfile(archive_path):
            with py7zr.SevenZipFile(archive_path, 'r') as zf:
                for name in zf.getnames():
                    internal_path = os.path.join(abs_archive_path, name).replace('\\', '/')
                    internal_files.append(internal_path)

        elif zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                for item in zf.infolist():
                    if not item.is_dir():
                        filename = deal_name_encoding(item.filename,os.path.basename(archive_path))
                        internal_path = os.path.join(abs_archive_path, filename).replace('\\', '/')
                        internal_files.append(internal_path)
        
    except (rarfile.NeedFirstVolume, rarfile.BadRarFile, rarfile.RarCannotExec,
            py7zr.exceptions.Bad7zFile, zipfile.BadZipFile, NotImplementedError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Unknown error processing archive: {e}\nfilename:{item.filename}\n")
        
    return internal_files


def process_directory(root_path):
    """
    遍历目录，处理文件和压缩包，返回成功和失败的列表。
    """
    success_list = []
    error_list = []

    if not os.path.isdir(root_path):
        error_list.append(f"Error: Provided path '{root_path}' is not a valid directory.")
        return [], error_list

    print(f"Starting scan in '{os.path.abspath(root_path)}'...")

    for root, _, files in os.walk(root_path):
        # 使用集合以便快速查找同目录下的文件
        files_in_current_dir = set(files)
        
        for filename in files:
            # 如果该文件已作为分卷的一部分被处理过，则跳过
            if filename in processed_volume_parts:
                continue

            full_path = os.path.join(root, filename)
            abs_path = os.path.abspath(full_path)

            try:
                # 1. 优先检查是否为分卷压缩包的起始文件
                volume_parts = (get_rar_volume_parts(full_path, files_in_current_dir) or
                                get_7z_volume_parts(full_path, files_in_current_dir) or
                                get_zip_volume_parts(full_path, files_in_current_dir))
                
                if volume_parts:
                    print(f"  -> Found volume set starting with: {full_path}, processing...")
                    success_list.extend(list_archive_files(full_path))
                    # 将此分卷的所有部分都加入已处理列表
                    processed_volume_parts.update(volume_parts)
                    continue # 处理完毕，进入下一个文件

                # 2. 如果不是分卷，再检查是否为普通单文件压缩包
                ext = os.path.splitext(filename)[1].lower()
                if ext in ['.rar', '.7z', '.zip']:
                    print(f"  -> Processing single archive: {full_path}")
                    success_list.extend(list_archive_files(full_path))
                else:
                    # 3. 如果都不是，则为普通文件
                    success_list.append(abs_path)

            except Exception as e:
                error_message = f"{abs_path} -> {type(e).__name__}: {e}"
                print(f"  [ERROR] {error_message}")
                error_list.append(error_message)

    return success_list, error_list


def main():
    """主函数"""
    if TARGET_PATH:
        scan_path = TARGET_PATH
    elif len(sys.argv) > 1:
        scan_path = sys.argv[1]
    else:
        print("Error: No target directory specified.")
        print(f"Usage: python {sys.argv[0]} <path_to_scan>")
        print(f"Or, edit the 'TARGET_PATH' variable inside the script.")
        return

    all_files, error_files = process_directory(scan_path)

    # 排序并写入成功列表
    print(f"\nSorting {len(all_files)} found file paths...")
    all_files.sort()
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for line in all_files:
                f.write(line + '\n')
        print(f"Successfully wrote {len(all_files)} paths to '{OUTPUT_FILE}'")
    except IOError as e:
        print(f"Error writing to '{OUTPUT_FILE}': {e}")

    # 写入错误列表
    if error_files:
        print(f"Found {len(error_files)} errors during scan.")
        try:
            with open(ERROR_FILE, 'w', encoding='utf-8') as f:
                for line in error_files:
                    f.write(line + '\n')
            print(f"Error details have been written to '{ERROR_FILE}'")
        except IOError as e:
            print(f"Error writing to '{ERROR_FILE}': {e}")
    else:
        print("Scan completed with no errors.")

if __name__ == "__main__":
    main()
