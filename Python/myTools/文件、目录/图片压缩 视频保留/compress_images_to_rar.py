#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片压缩、视频保留

用法：
    python compress_images_to_rar.py              # 处理脚本自身所在目录
    python compress_images_to_rar.py D:\\某目录    # 处理指定目录
    python compress_images_to_rar.py --dry-run    # 只预览，不动文件

规则（递归获取所有子目录，由深到浅逐个判断）：
    1. 目录内只有图片            -> 把整个目录压缩成 <父目录>\\<目录名>.rar，原目录删除
    2. 目录内有图片 + 其他内容   -> 只把图片压缩成 <目录>\\图片.rar，图片删除，
                                    目录本身与其余内容（视频、文档、子目录等）全部保留
    3. 目录内没有图片            -> 跳过，不做任何处理

    压缩与删除原文件都由硬编码的 Rar.exe 完成，删除走的是 rar 的 -df 参数
    （文件成功写入压缩包之后才会被删除）。
"""

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

# ==================== 配置区 ====================

# winrar 自带的命令行版 rar.exe，硬编码指定
RAR_EXE = r"D:\P\WinRAR\Rar.exe"

# rar 参数：-y 全部确认（非交互）、-dh 允许处理被其他程序占用的文件、
#           -df 压缩完成后删除原文件、-m5 最大压缩率
# 注意：图片本身已经是压缩格式，-m5 对体积几乎没有帮助却很慢，
#       想快可以换成 -m0（仅存储）或 -m1（最快）
RAR_FLAGS = ["-y", "-dh", "-m0"]

# “只有图片”的目录里，图片压缩包的文件名
IMAGE_RAR_NAME = "图片.rar"

# 日志文件名，写在脚本所在目录
LOG_FILE_NAME = "compress_images_to_rar.log"

IMAGE_EXTS = {
    ".jpg", ".jpeg", ".jpe", ".jfif", ".png", ".gif", ".bmp", ".webp",
    ".tif", ".tiff", ".heic", ".heif", ".avif", ".ico", ".svg", ".psd",
    ".raw", ".cr2", ".cr3", ".nef", ".arw", ".dng", ".orf", ".rw2",
    ".pef", ".raf", ".sr2", ".mrw", ".x3f",
}

# 视频扩展名只用于统计和日志提示；视频不会被压缩，也不会被删除
VIDEO_EXTS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v",
    ".mpg", ".mpeg", ".m2ts", ".mts", ".ts", ".rmvb", ".rm", ".3gp",
    ".vob", ".f4v", ".ogv", ".asf", ".divx",
}

logger = logging.getLogger("compress_to_rar")


def setup_logger(log_file: Path):
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as e:
        logger.warning("无法创建日志文件 %s: %s", log_file, e)


def decode_output(data: bytes) -> str:
    """Rar.exe 在中文 Windows 下按 GBK 输出，这里做个兼容解码。"""
    for encoding in ("utf-8", "gbk"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def run_rar(args, cwd: Path) -> bool:
    """在 cwd 目录下执行 rar，成功（返回码 0/1）返回 True。"""
    cmd = [RAR_EXE] + args
    logger.info("  执行: %s", subprocess.list2cmdline(cmd))
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as e:
        logger.error("  启动 Rar.exe 失败: %s", e)
        return False

    for line in decode_output(proc.stdout).splitlines():
        line = line.strip()
        if line:
            logger.info("  [rar] %s", line)

    # 0=成功 1=有警告但不影响压缩结果，其余都当作失败
    if proc.returncode in (0, 1):
        return True
    logger.error("  Rar.exe 返回码 %s，视为失败", proc.returncode)
    return False


def collect_subdirs(root: Path):
    """递归收集 root 下所有子目录（不含 root 自身），按层级由深到浅排序。"""
    subdirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        if current == root:
            continue
        subdirs.append(current)
    # 深的先处理，避免父目录先被压缩掉之后子目录判断出错
    subdirs.sort(key=lambda p: len(p.parts), reverse=True)
    return subdirs


def classify(directory: Path):
    """把目录的直接内容分成『图片』和『其他内容』两类（其他内容含子目录）。"""
    images, others = [], []
    for entry in directory.iterdir():
        if entry.is_file() and entry.suffix.lower() in IMAGE_EXTS:
            images.append(entry)
        else:
            others.append(entry)
    return images, others


def remove_empty_tree(directory: Path):
    """自底向上删除空目录，压缩完成后清掉已经空掉的原目录。"""
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        current = Path(dirpath)
        try:
            if not any(current.iterdir()):
                current.rmdir()
                logger.info("  已删除空目录: %s", current)
        except OSError as e:
            logger.warning("  删除空目录失败: %s (%s)", current, e)


def archive_whole_dir(directory: Path):
    """整个目录压缩成 <父目录>\\<目录名>.rar，然后删掉原目录。"""
    archive = directory.parent / (directory.name + ".rar")
    if archive.exists():
        logger.info("  压缩包已存在，将追加/更新: %s", archive)

    # 以父目录为工作目录，参数用相对名，压缩包里就是 <目录名>\\... 的结构
    ok = run_rar(
        ["a"] + RAR_FLAGS + ["-df", archive.name, directory.name],
        directory.parent,
    )
    if ok:
        remove_empty_tree(directory)
    else:
        logger.error("  压缩失败，保留原目录不删除: %s", directory)
    return ok


def archive_images(directory: Path):
    """只把目录里的图片压缩成 图片.rar，其余文件原样保留。"""
    masks = ["*" + ext for ext in sorted(IMAGE_EXTS)]
    # 不加 -r，所以掩码只匹配当前目录下的文件，不会碰到子目录
    ok = run_rar(
        ["a"] + RAR_FLAGS + ["-df", IMAGE_RAR_NAME] + masks,
        directory,
    )
    if not ok:
        logger.error("  压缩失败: %s", directory)
    return ok


def process(root: Path, dry_run: bool):
    subdirs = collect_subdirs(root)
    logger.info("根目录: %s", root)
    logger.info("共发现 %d 个子目录，按由深到浅的顺序处理", len(subdirs))

    whole_dirs = 0
    image_dirs = 0
    skipped = 0
    failed = 0

    for directory in subdirs:
        if not directory.is_dir():
            continue  # 已经被之前处理子目录时删掉了

        images, others = classify(directory)

        if not images:
            skipped += 1
            continue

        if not others:
            # 目录里清一色是图片 -> 整个目录打包
            whole_dirs += 1
            logger.info("[整目录压缩] %s  (图片 %d 个，无其他内容)", directory, len(images))
            if dry_run:
                logger.info(
                    "  [DRY-RUN] rar a %s -df \"%s\" \"%s\"  (工作目录: %s)",
                    " ".join(RAR_FLAGS), directory.name + ".rar", directory.name,
                    directory.parent,
                )
                continue
            if not archive_whole_dir(directory):
                failed += 1
        else:
            # 有图片也有别的东西 -> 只压缩图片
            image_dirs += 1
            videos = [
                p for p in others
                if p.is_file() and p.suffix.lower() in VIDEO_EXTS
            ]
            logger.info(
                "[仅压缩图片] %s  (图片 %d 个；其他内容 %d 个，其中视频 %d 个)",
                directory, len(images), len(others), len(videos),
            )
            if dry_run:
                logger.info(
                    "  [DRY-RUN] rar a %s -df \"%s\" <图片掩码>  (工作目录: %s)",
                    " ".join(RAR_FLAGS), IMAGE_RAR_NAME, directory,
                )
                continue
            if archive_images(directory):
                leftover = [p.name for p in images if p.exists()]
                if leftover:
                    logger.warning(
                        "  以下图片没有被删除（可能被占用或未成功入包）: %s",
                        ", ".join(leftover),
                    )
            else:
                failed += 1

    logger.info("=" * 70)
    logger.info("处理完成%s", "（DRY-RUN，未改动任何文件）" if dry_run else "")
    logger.info("整个目录压缩: %d 个", whole_dirs)
    logger.info("仅压缩图片:   %d 个", image_dirs)
    logger.info("跳过(无图片): %d 个", skipped)
    logger.info("失败:         %d 个", failed)


def main():
    parser = argparse.ArgumentParser(description="图片压缩为 rar，视频等其他内容保留")
    parser.add_argument(
        "root",
        nargs="?",
        default=None,
        help="要处理的根目录，默认为脚本自身所在目录",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要执行的操作，不实际压缩和删除",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = Path(args.root).resolve() if args.root else script_dir

    setup_logger(script_dir / LOG_FILE_NAME)

    if not Path(RAR_EXE).is_file():
        logger.error("找不到 rar.exe，请修改脚本顶部的 RAR_EXE 常量: %s", RAR_EXE)
        sys.exit(1)
    if not root.is_dir():
        logger.error("根目录不存在或不是目录: %s", root)
        sys.exit(1)

    logger.info("=" * 70)
    logger.info("rar.exe: %s", RAR_EXE)
    logger.info("rar 参数: %s", " ".join(RAR_FLAGS))
    if args.dry_run:
        logger.info("运行模式: DRY-RUN（不会修改任何文件）")

    process(root, args.dry_run)


if __name__ == "__main__":
    main()
