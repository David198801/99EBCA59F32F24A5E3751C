import os
import re
import subprocess
from pathlib import Path

# =========================
# 硬编码配置
# =========================
ROOT_DIR = r"E:\BaiduNetdiskDownload\伊ヶ崎綾香nicochannel录播 [241.01G]pw伊ヶ崎綾香\伊ヶ崎綾香"

PASSWORD_LIST = [
    "伊ヶ崎綾香",
    ""
]

# 是否删除解压成功后的压缩包（默认不删）
DELETE_ARCHIVE_AFTER_SUCCESS = False


# =========================
# 工具函数
# =========================
def is_supported_archive(filename: str) -> bool:
    name = filename.lower()

    if name.endswith(".zip") or name.endswith(".7z") or name.endswith(".rar"):
        return True

    # 分卷场景
    if re.search(r"\.zip\.\d{3}$", name):
        return True
    if re.search(r"\.7z\.\d{3}$", name):
        return True

    # rar 旧式分卷：.r00 .r01 ...
    if re.search(r"\.r\d{2}$", name):
        return True

    return False


def is_first_volume(path: Path) -> bool:
    """
    判断是否是应该处理的“主卷”：
    - 普通 zip/7z/rar：处理
    - .7z.001 / .zip.001：处理
    - .7z.002 / .zip.002：跳过
    - part1.rar / part01.rar：处理
    - part2.rar 及后续：跳过
    - .r00 / .r01：跳过（依赖主 .rar）
    """
    name = path.name.lower()

    # zip 分卷
    m = re.search(r"\.zip\.(\d{3})$", name)
    if m:
        return m.group(1) == "001"

    # 7z 分卷
    m = re.search(r"\.7z\.(\d{3})$", name)
    if m:
        return m.group(1) == "001"

    # rar 旧式分卷 .r00 .r01 跳过
    if re.search(r"\.r\d{2}$", name):
        return False

    # rar 新式分卷 xxx.part1.rar / xxx.part01.rar
    m = re.search(r"\.part(\d+)\.rar$", name)
    if m:
        return int(m.group(1)) == 1

    # 普通 .rar / .zip / .7z
    if name.endswith(".rar") or name.endswith(".zip") or name.endswith(".7z"):
        return True

    return False


def collect_archives(root_dir: str):
    result = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if is_supported_archive(file):
                p = Path(root) / file
                if is_first_volume(p):
                    result.append(p)
    return result


def test_archive(archive_path: Path, password: str) -> bool:
    """
    用 7z t 测试压缩包是否可以用当前密码正常读取
    """
    cmd = [
        "7z",
        "t",
        str(archive_path),
        f"-p{password}",
        "-y",
    ]
    completed = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    output = completed.stdout.lower()

    # 7z 返回码 0 一般表示成功
    if completed.returncode == 0:
        return True

    # 某些情况下通过输出再辅助判断
    if "everything is ok" in output:
        return True

    return False


def extract_archive(archive_path: Path, password: str) -> bool:
    """
    解压到原目录
    -x: 解压带完整路径
    -o: 输出目录为原目录
    -aou: 文件重名自动重命名
    """
    out_dir = archive_path.parent

    cmd = [
        "7z",
        "x",
        str(archive_path),
        f"-o{out_dir}",
        f"-p{password}",
        "-y",
        "-aou",
    ]

    completed = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    output = completed.stdout.lower()

    if completed.returncode == 0:
        return True

    if "everything is ok" in output:
        return True

    return False


def try_extract_with_passwords(archive_path: Path, passwords) -> bool:
    for pwd in passwords:
        print(f"  尝试密码: {repr(pwd)}")
        if test_archive(archive_path, pwd):
            print(f"  测试成功，开始解压: {archive_path}")
            if extract_archive(archive_path, pwd):
                print(f"  解压成功: {archive_path}")
                return True
            else:
                print(f"  解压失败(测试成功但解压失败): {archive_path}")
        else:
            print(f"  密码不对或压缩包测试失败: {archive_path}")
    return False


def main():
    root = Path(ROOT_DIR)

    if not root.exists():
        print(f"路径不存在: {root}")
        return

    archives = collect_archives(str(root))

    if not archives:
        print("未找到压缩包")
        return

    print(f"共找到 {len(archives)} 个待处理压缩包/主卷\n")

    success_count = 0
    fail_count = 0

    for archive in archives:
        print("=" * 80)
        print(f"处理: {archive}")

        ok = try_extract_with_passwords(archive, PASSWORD_LIST)

        if ok:
            success_count += 1
            if DELETE_ARCHIVE_AFTER_SUCCESS:
                try:
                    archive.unlink()
                    print(f"已删除压缩包: {archive}")
                except Exception as e:
                    print(f"删除失败: {archive}, 错误: {e}")
        else:
            fail_count += 1
            print(f"最终失败: {archive}")

    print("\n" + "=" * 80)
    print(f"处理完成")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")


if __name__ == "__main__":
    main()
