# -*- coding: utf-8 -*-
"""
按文件内容去重脚本（可复用）。

用法:
    python dedupe_files.py [源目录]

规则:
  1. 递归扫描源目录下所有文件（排除输出目录和日志文件本身）。
  2. 按内容哈希判断重复（先比大小，再比 SHA256）。
  3. 唯一文件 → 去重后/<相对路径>
  4. 重复的一组: 保留一份 → 去重后/<相对路径>，其余 → 重复文件/<相对路径>
     组内保留哪一份: 优先保留不带 “(1)” 这类自动重命名后缀的文件
     （如 a.txt 优先于 a (1).txt），其余按路径排序保证可复现。
  5. 移动策略（递归）:
     - 整个子树的文件都去“去重后”时，直接递归移动整个文件夹；
     - 含重复文件的文件夹才拆开逐个移动文件，保留相对路径结构。
  6. 全部移动完成后，自底向上清理源目录残留的空文件夹。
  7. 日志同时输出到控制台和 去重日志.log（UTF-8），重复文件按组逐条记录。
"""

import argparse
import hashlib
import logging
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

CHUNK_SIZE = 1024 * 1024
UNIQUE_DIR = "去重后"
DUPLICATE_DIR = "重复文件"
LOG_FILE = "去重日志.log"

# 浏览器/系统自动重命名产生的副本后缀，如 "a (1)"、"a(2)"
COPY_SUFFIX_RE = re.compile(r" ?\(\d+\)$")

LOGGER = logging.getLogger("dedupe")
_SOURCE = Path(".")


def file_hash(path: Path) -> str:
    """计算文件内容的 SHA256。"""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK_SIZE), b""):
            h.update(block)
    return h.hexdigest()


def is_excluded(path: Path, output_dirs: set) -> bool:
    """输出目录本身及其内部的路径、以及日志文件，都不参与去重。"""
    if path in output_dirs:
        return True
    if path.name == LOG_FILE:
        return True
    return any(parent in output_dirs for parent in path.parents)


def keeper_priority(path: Path) -> tuple:
    """组内排序: 不带 “(1)” 后缀的文件优先保留，其次按路径排序。"""
    is_auto_copy = 1 if COPY_SUFFIX_RE.search(path.stem) else 0
    return (is_auto_copy, str(path))


def rel(path: Path) -> str:
    """转为相对源目录的路径，便于日志阅读。"""
    try:
        return str(path.relative_to(_SOURCE))
    except ValueError:
        return str(path)


def setup_logging(source: Path) -> None:
    """控制台 + 日志文件双输出（统一 UTF-8，避免中文乱码）。"""
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(source / LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(fmt)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)


def scan_files(source: Path, output_dirs: set):
    """递归列出源目录下的文件，跳过输出目录和日志文件。"""
    for path in sorted(source.rglob("*")):
        if path.is_file() and not is_excluded(path, output_dirs):
            yield path


def safe_move_file(src: Path, dest: Path) -> None:
    """移动单个文件；目标重名时自动加序号防覆盖。"""
    if dest.exists():
        stem, suffix = dest.stem, dest.suffix
        n = 1
        while dest.with_name(f"{stem}_{n}{suffix}").exists():
            n += 1
        dest = dest.with_name(f"{stem}_{n}{suffix}")
        LOGGER.info("目标已存在，自动重命名: %s", rel(dest))
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    LOGGER.info("移动文件: %s -> %s", rel(src), rel(dest))


def move_tree(src: Path, dest: Path) -> None:
    """递归移动整个文件夹（保留结构）；目标已存在则逐项合并进去。"""
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        LOGGER.info("整体递归移动文件夹: %s -> %s", rel(src), rel(dest))
        return
    LOGGER.info("目标文件夹已存在，逐项合并: %s -> %s", rel(src), rel(dest))
    for child in sorted(src.iterdir()):
        if child.is_dir():
            move_tree(child, dest / child.name)
        else:
            safe_move_file(child, dest / child.name)
    # 走到这里 src 已被掏空，由最后的清理步骤删除


def prune_empty_dirs(source: Path, output_dirs: set) -> int:
    """自底向上删除残留的空文件夹，返回删除数量。"""
    removed = 0
    dirs = [
        p for p in source.rglob("*")
        if p.is_dir() and not is_excluded(p, output_dirs)
    ]
    # 按路径深度从深到浅排序，先删子目录才能删父目录
    for d in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
        try:
            next(d.iterdir())  # 目录非空时不会抛 StopIteration
        except StopIteration:
            d.rmdir()
            removed += 1
            LOGGER.info("删除空文件夹: %s", rel(d))
        except OSError:
            LOGGER.warning("跳过（无法删除）: %s", rel(d))
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="按内容去重：保留一份在“去重后”，其余移到“重复文件”"
    )
    parser.add_argument("source", nargs="?", default=".", help="源目录（默认当前目录）")
    args = parser.parse_args()

    global _SOURCE
    _SOURCE = Path(args.source).resolve()
    source = _SOURCE
    if not source.is_dir():
        print(f"错误: 源目录不存在: {source}", file=sys.stderr)
        return 1

    setup_logging(source)

    out_unique = source / UNIQUE_DIR
    out_dup = source / DUPLICATE_DIR
    output_dirs = {out_unique, out_dup}
    out_unique.mkdir(exist_ok=True)
    out_dup.mkdir(exist_ok=True)

    # 1. 扫描 + 按 (大小, 哈希) 分组
    groups = defaultdict(list)  # key: (size, sha256) -> [路径...]
    total = 0
    for path in scan_files(source, output_dirs):
        groups[(path.stat().st_size, file_hash(path))].append(path)
        total += 1

    if total == 0:
        LOGGER.info("未发现可处理的文件。")

    # 2. 规划每个文件的去向: 源路径 -> (目标根目录, 相对路径)，并按组输出重复日志
    dests = {}
    dup_groups = 0
    group_no = 0
    for (size, sha), paths in sorted(groups.items(), key=lambda kv: str(kv[1][0])):
        # 组内排序: 不带 "(1)" 的在前，保证它被保留
        paths.sort(key=keeper_priority)

        if len(paths) == 1:
            src = paths[0]
            dests[src] = (out_unique, src.relative_to(source))
            continue

        dup_groups += 1
        group_no += 1
        has_auto_copy = any(COPY_SUFFIX_RE.search(p.stem) for p in paths)
        LOGGER.info(
            "重复组 #%d: %d 个文件内容完全相同 | 大小 %d 字节 | SHA256=%s",
            group_no, len(paths), size, sha,
        )
        for i, src in enumerate(paths):
            r = src.relative_to(source)
            if i == 0:
                dests[src] = (out_unique, r)
                hint = "（优先保留不带(1)的）" if has_auto_copy else ""
                LOGGER.info("  [保留] %s -> %s/%s %s", r, UNIQUE_DIR, r, hint)
            else:
                dests[src] = (out_dup, r)
                LOGGER.info("  [重复] %s -> %s/%s", r, DUPLICATE_DIR, r)

    # 3. 递归移动
    def subtree_all_unique(d: Path) -> bool:
        """子树内所有文件是否都去“去重后”（可整体递归移动）。"""
        for p in d.rglob("*"):
            if p.is_file() and not is_excluded(p, output_dirs):
                root, _ = dests[p]
                if root is not out_unique:
                    return False
        return True

    def move_dir(d: Path, r: Path) -> None:
        if subtree_all_unique(d):
            move_tree(d, out_unique / r)  # 整个文件夹一次性递归移动
            return
        # 含重复文件，拆开处理：能整体移动的子树仍整体移动
        for child in sorted(d.iterdir()):
            if is_excluded(child, output_dirs):
                continue
            if child.is_dir():
                move_dir(child, r / child.name)
            elif child in dests:
                root, dr = dests[child]
                safe_move_file(child, root / dr)

    for entry in sorted(source.iterdir()):
        if is_excluded(entry, output_dirs):
            continue
        if entry.is_dir():
            move_dir(entry, Path(entry.name))
        elif entry in dests:
            root, dr = dests[entry]
            safe_move_file(entry, root / dr)

    # 4. 清理移动后残留的空文件夹
    removed_dirs = prune_empty_dirs(source, output_dirs)

    # 5. 汇总
    unique_single = sum(1 for paths in groups.values() if len(paths) == 1)
    kept = dup_groups
    moved_dup = total - unique_single - dup_groups
    LOGGER.info("=" * 50)
    LOGGER.info("扫描文件总数 : %d", total)
    LOGGER.info("重复组数     : %d", dup_groups)
    LOGGER.info("去重后 (唯一): %d", unique_single)
    LOGGER.info("去重后 (每组保留一份): %d", kept)
    LOGGER.info("重复文件     : %d", moved_dup)
    LOGGER.info("清理空文件夹 : %d", removed_dirs)
    LOGGER.info("日志文件     : %s", rel(source / LOG_FILE))
    LOGGER.info("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
