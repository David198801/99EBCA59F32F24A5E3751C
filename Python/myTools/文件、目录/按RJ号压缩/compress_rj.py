"""
如E:\test\RJ123456 sfe sfe sef
会压缩成E:\test\RJ123456 sfe sfe sef\RJ123456.rar
"""

import os
import re
import subprocess

# ==================== 硬编码配置 ====================
ROOT_DIR = r"E:\BaiduNetdiskDownload\temp\新建文件夹"                        # 要处理的根目录
RAR_EXE  = r"D:\P\WinRAR\rar.exe"    # rar.exe 完整路径
# ==================================================

# 匹配 RJ + 6~8位数字（忽略大小写）
RJ_PATTERN = re.compile(r'RJ(\d{6,8})', re.IGNORECASE)


def main():
    if not os.path.isdir(ROOT_DIR):
        print(f"错误：根目录不存在 -> {ROOT_DIR}")
        return
    if not os.path.isfile(RAR_EXE):
        print(f"错误：rar.exe 不存在 -> {RAR_EXE}")
        return

    # 遍历根目录下的直接子目录
    for entry in os.scandir(ROOT_DIR):
        if not entry.is_dir():
            continue

        subdir_name = entry.name
        subdir_path = entry.path

        # 从子目录名中提取第一个 RJ 号
        match = RJ_PATTERN.search(subdir_name)
        if not match:
            print(f"跳过（未找到RJ号）：{subdir_name}")
            continue

        rj_number = f"RJ{match.group(1)}"          # 统一大写 RJ
        rar_name = f"{rj_number}.rar"
        rar_path = os.path.join(subdir_path, rar_name)   # 压缩包放在子目录内

        # 如果目标 rar 已存在，跳过避免覆盖
        if os.path.exists(rar_path):
            print(f"跳过（目标已存在）：{subdir_name}\\{rar_name}")
            continue

        print(f"正在压缩并删除原文件：{subdir_name}  ->  {subdir_name}\\{rar_name}")

        # 在子目录中运行 rar：
        #   a      添加文件到压缩包
        #   -r     递归包含子目录
        #   -y     全部确认
        #   -df    压缩成功后删除被压缩的源文件（及压缩后为空的子目录）
        # 输出文件用相对名 rar_name，写在当前工作目录（即 subdir_path）里。
        try:
            result = subprocess.run(
                [RAR_EXE, "a", "-r", "-y", "-df", rar_name, "."],
                cwd=subdir_path,
                capture_output=True,
                text=True,
                encoding="gbk",      # Windows 下 rar 输出通常为 GBK
                errors="ignore"
            )
        except Exception as e:
            print(f"  调用 rar 失败：{e}")
            continue

        # rar 返回码：0 成功，1 警告，其他为错误
        if result.returncode not in (0, 1):
            print(f"  压缩失败，返回码 {result.returncode}")
            print(result.stdout)
            print(result.stderr)
            continue

        print(f"  完成：{subdir_name}\\{rar_name}")

    print("全部处理完毕。")


if __name__ == "__main__":
    main()