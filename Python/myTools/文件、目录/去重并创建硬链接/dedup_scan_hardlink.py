"""
使用方法
python dedup_scan_hardlink.py E:\a --min-size 30MB --dry-run
python dedup_scan_hardlink.py E:\a --min-size 30MB --execute

清理 share 目录中没有外部硬链接关联的文件：
python dedup_scan_hardlink.py E:\a --clean
"""

import os
import sys
import time
import json
import hashlib
import shutil
import argparse
import logging
from pathlib import Path
from collections import defaultdict

HASH_CHUNK_SIZE = 8 * 1024 * 1024  # 8MB
SHARE_DIR_NAME = "share_dedup"
DEFAULT_CACHE_FILE = "dedup_hash_cache.json"


def setup_logger(log_file: Path):
    logger = logging.getLogger("dedup")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def load_cache(cache_file: Path, logger):
    if not cache_file.exists():
        logger.info(f"缓存文件不存在，将新建缓存: {cache_file}")
        return {}

    try:
        with cache_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            logger.warning(f"缓存文件格式不正确，将忽略并重建: {cache_file}")
            return {}
        logger.info(f"已加载缓存文件: {cache_file}，缓存条目数: {len(data)}")
        return data
    except Exception as e:
        logger.error(f"加载缓存文件失败，将使用空缓存: {cache_file}, 错误: {e}")
        return {}


def save_cache(cache_file: Path, cache_data: dict, logger):
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        tmp_file = cache_file.with_suffix(cache_file.suffix + ".tmp")
        with tmp_file.open("w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        tmp_file.replace(cache_file)
        logger.info(f"缓存已保存: {cache_file}，缓存条目数: {len(cache_data)}")
    except Exception as e:
        logger.error(f"保存缓存失败: {cache_file}, 错误: {e}")


def get_file_cache_key(path: Path) -> str:
    return str(path.resolve())


def get_file_signature(path: Path):
    st = path.stat()
    return {
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
    }


def get_share_dir(scan_root: Path) -> Path:
    """
    根据扫描目录自动生成 share 目录：
    例如:
      E:\\AI -> E:\\share_dedup
      D:\\data\\abc -> D:\\share_dedup
    """
    drive = os.path.splitdrive(str(scan_root.resolve()))[0]
    if not drive:
        raise ValueError(f"无法识别扫描目录所在盘符: {scan_root}")
    return Path(f"{drive}\\{SHARE_DIR_NAME}")


def same_volume(p1: Path, p2: Path) -> bool:
    d1 = os.path.splitdrive(str(p1.resolve()))[0].lower()
    d2 = os.path.splitdrive(str(p2.resolve()))[0].lower()
    return d1 == d2


def safe_filename(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for c in invalid_chars:
        name = name.replace(c, "_")
    return name


def file_blake2b(path: Path) -> str:
    h = hashlib.blake2b()
    with path.open("rb") as f:
        while True:
            chunk = f.read(HASH_CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def get_file_hash_with_cache(path: Path, cache_data: dict, logger) -> str:
    cache_key = get_file_cache_key(path)

    try:
        sig = get_file_signature(path)
    except Exception as e:
        logger.error(f"读取文件签名失败: {path}, 错误: {e}")
        raise

    cached = cache_data.get(cache_key)
    if cached:
        if (
            isinstance(cached, dict)
            and cached.get("size") == sig["size"]
            and cached.get("mtime_ns") == sig["mtime_ns"]
            and "hash" in cached
        ):
            logger.info(f"缓存命中，直接复用 hash: {path}")
            return cached["hash"]
        else:
            logger.info(f"缓存失效，重新计算 hash: {path}")

    file_hash = file_blake2b(path)
    cache_data[cache_key] = {
        "size": sig["size"],
        "mtime_ns": sig["mtime_ns"],
        "hash": file_hash,
    }
    logger.info(f"新计算 hash 并写入缓存: {path}")
    return file_hash


def ensure_share_file_path(share_dir: Path, src_path: Path, file_hash: str) -> Path:
    ext = src_path.suffix
    stem = safe_filename(src_path.stem)
    filename = f"{file_hash}_{stem}{ext}"
    return share_dir / filename


def scan_files(root: Path, min_size: int, share_dir: Path, logger):
    files = []
    logger.info(f"开始扫描目录: {root}")
    logger.info(f"仅处理大小 >= {min_size} 字节 的文件")
    logger.info(f"自动使用 share 目录: {share_dir}")

    share_dir_resolved = share_dir.resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        current_dir = Path(dirpath)

        # 防止扫描进入 share 目录
        try:
            if current_dir.resolve() == share_dir_resolved:
                logger.info(f"跳过 share 目录: {current_dir}")
                dirnames[:] = []
                continue
        except Exception:
            pass

        for name in filenames:
            path = current_dir / name
            try:
                if not path.is_file():
                    continue

                # 防止误处理 share 目录下文件
                try:
                    if share_dir_resolved in path.resolve().parents or path.resolve() == share_dir_resolved:
                        logger.info(f"跳过 share 内文件: {path}")
                        continue
                except Exception:
                    pass

                size = path.stat().st_size
                if size < min_size:
                    continue

                files.append(path)
            except Exception as e:
                logger.error(f"扫描文件失败: {path}, 错误: {e}")

    logger.info(f"扫描完成，候选文件数: {len(files)}")
    return files


def group_by_size(paths, logger):
    size_map = defaultdict(list)
    for path in paths:
        try:
            size = path.stat().st_size
            size_map[size].append(path)
        except Exception as e:
            logger.error(f"读取文件大小失败: {path}, 错误: {e}")
    logger.info(f"按大小分组完成，共 {len(size_map)} 个 size 分组")
    return size_map


def group_by_hash(size_map, logger, cache_data):
    hash_map = defaultdict(list)

    candidate_groups = 0
    candidate_files = 0
    cache_hit_count = 0
    hash_calc_count = 0

    for size, group in size_map.items():
        if len(group) <= 1:
            continue

        candidate_groups += 1
        candidate_files += len(group)

        logger.info(f"发现大小重复组: size={size}, count={len(group)}，开始计算 hash")

        for i, path in enumerate(group, 1):
            try:
                cache_key = get_file_cache_key(path)
                old_entry = cache_data.get(cache_key)

                file_hash = get_file_hash_with_cache(path, cache_data, logger)
                key = (size, file_hash)
                hash_map[key].append(path)

                new_entry = cache_data.get(cache_key)
                if old_entry and old_entry == new_entry:
                    cache_hit_count += 1
                else:
                    hash_calc_count += 1

                logger.info(f"  [{i}/{len(group)}] 已得到 hash: {path}")
            except Exception as e:
                logger.error(f"计算 hash 失败: {path}, 错误: {e}")

    logger.info(f"需要计算 hash 的大小重复组数量: {candidate_groups}")
    logger.info(f"需要计算 hash 的文件数量: {candidate_files}")
    logger.info(f"缓存命中数量: {cache_hit_count}")
    logger.info(f"实际计算 hash 数量: {hash_calc_count}")
    return hash_map


def samefile_safe(a: Path, b: Path) -> bool:
    try:
        return os.path.samefile(a, b)
    except Exception:
        return False


def move_and_link_group(group, share_dir: Path, logger, cache_data, dry_run=False):
    """
    group: 内容完全相同的一组文件
    处理逻辑：
      1. 选择第一份作为 canonical
      2. 移动到 share 目录
      3. 所有原路径创建硬链接到 share 文件
    """
    if len(group) <= 1:
        return 0

    canonical_src = group[0]

    try:
        size = canonical_src.stat().st_size
        file_hash = get_file_hash_with_cache(canonical_src, cache_data, logger)
    except Exception as e:
        logger.error(f"无法获取 canonical 文件信息: {canonical_src}, 错误: {e}")
        return 0

    share_target = ensure_share_file_path(share_dir, canonical_src, file_hash)

    logger.info("=" * 80)
    logger.info(f"处理重复文件组: count={len(group)}, size={size}, hash={file_hash}")
    for p in group:
        logger.info(f"  {p}")
    logger.info(f"share 目标文件: {share_target}")

    if not same_volume(canonical_src, share_target):
        logger.warning(f"canonical 文件与 share 不在同一盘符，跳过该组: {canonical_src} -> {share_target}")
        return 0

    if dry_run:
        logger.info("[DRY-RUN] 将确保 share 目录存在")
    else:
        share_dir.mkdir(parents=True, exist_ok=True)

    # 先确保 share 目标文件存在
    if share_target.exists():
        try:
            share_size = share_target.stat().st_size
            share_hash = get_file_hash_with_cache(share_target, cache_data, logger)
            if share_size != size or share_hash != file_hash:
                logger.error(f"share 目录中已存在同名文件但内容不同，跳过: {share_target}")
                return 0
            else:
                logger.info(f"share 文件已存在且内容一致: {share_target}")
        except Exception as e:
            logger.error(f"校验 share 文件失败: {share_target}, 错误: {e}")
            return 0
    else:
        if dry_run:
            logger.info(f"[DRY-RUN] 将移动 canonical 文件到 share: {canonical_src} -> {share_target}")
        else:
            try:
                share_target.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"移动 canonical 文件到 share: {canonical_src} -> {share_target}")
                shutil.move(str(canonical_src), str(share_target))

                # 更新缓存：旧路径删除，新路径继承缓存
                old_key = get_file_cache_key(canonical_src)
                new_key = str(share_target.resolve())
                if old_key in cache_data:
                    cache_data[new_key] = cache_data.pop(old_key)
                else:
                    try:
                        sig = get_file_signature(share_target)
                        cache_data[new_key] = {
                            "size": sig["size"],
                            "mtime_ns": sig["mtime_ns"],
                            "hash": file_hash,
                        }
                    except Exception:
                        pass

            except Exception as e:
                logger.error(f"移动 canonical 文件失败: {canonical_src} -> {share_target}, 错误: {e}")
                return 0

    linked_count = 0

    # 为所有原始路径创建硬链接
    for src in group:
        try:
            if not same_volume(src, share_target):
                logger.warning(f"源文件与 share 不在同一盘符，跳过: {src} -> {share_target}")
                continue

            if src == share_target:
                logger.info(f"跳过 share 文件本身: {src}")
                continue

            if src.exists() and samefile_safe(src, share_target):
                logger.info(f"已是同一个硬链接，跳过: {src}")
                continue

            if dry_run:
                if src.exists():
                    logger.info(f"[DRY-RUN] 将删除原文件: {src}")
                logger.info(f"[DRY-RUN] 将创建硬链接: {src} -> {share_target}")
                linked_count += 1
            else:
                if src.exists():
                    logger.info(f"删除原文件: {src}")
                    src.unlink()

                src.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"创建硬链接: {src} -> {share_target}")
                os.link(str(share_target), str(src))
                linked_count += 1

                # 更新缓存：硬链接新路径直接复用 hash 信息
                try:
                    sig = get_file_signature(src)
                    cache_data[get_file_cache_key(src)] = {
                        "size": sig["size"],
                        "mtime_ns": sig["mtime_ns"],
                        "hash": file_hash,
                    }
                except Exception:
                    pass

        except Exception as e:
            logger.error(f"创建硬链接失败: {src} -> {share_target}, 错误: {e}")

    return linked_count


def dedup(root: Path, min_size: int, share_dir: Path, logger, dry_run: bool, cache_data: dict):
    start = time.time()

    files = scan_files(root, min_size, share_dir, logger)
    size_map = group_by_size(files, logger)
    hash_map = group_by_hash(size_map, logger, cache_data)

    dup_groups = 0
    dup_files = 0
    total_saved_bytes = 0

    for (size, file_hash), group in hash_map.items():
        if len(group) <= 1:
            continue

        dup_groups += 1
        dup_files += len(group)

        move_and_link_group(group, share_dir, logger, cache_data, dry_run=dry_run)

        # 节省空间 = (重复份数 - 1) * 文件大小
        total_saved_bytes += (len(group) - 1) * size

    elapsed = time.time() - start

    logger.info("=" * 80)
    logger.info("处理完成")
    logger.info(f"模式: {'DRY-RUN' if dry_run else 'EXECUTE'}")
    logger.info(f"扫描目录: {root}")
    logger.info(f"share 目录: {share_dir}")
    logger.info(f"最小文件大小阈值: {min_size} 字节")
    logger.info(f"重复组数量: {dup_groups}")
    logger.info(f"重复文件数量: {dup_files}")
    logger.info(f"预计/实际节省空间: {total_saved_bytes} 字节 ({total_saved_bytes / 1024 / 1024 / 1024:.2f} GB)")
    logger.info(f"耗时: {elapsed:.2f} 秒")


def clean_share_dir(share_dir: Path, logger, cache_data: dict):
    """
    清理 share 目录中没有外部硬链接关联的文件。

    判断标准：
      Windows / NTFS 下 stat().st_nlink 表示硬链接数量。
      如果 st_nlink <= 1，说明这个文件只有 share 目录中的这一份，
      没有任何原始路径再链接到它，可以删除。

    注意：
      st_nlink == 1：孤儿 share 文件，可以删除
      st_nlink >= 2：仍有其他硬链接关联，保留
    """
    start = time.time()

    logger.info("=" * 80)
    logger.info("启动 CLEAN 模式")
    logger.info(f"share 目录: {share_dir}")

    if not share_dir.exists():
        logger.warning(f"share 目录不存在，无需清理: {share_dir}")
        return

    if not share_dir.is_dir():
        logger.error(f"share 路径不是目录，无法清理: {share_dir}")
        return

    total_files = 0
    orphan_files = 0
    deleted_files = 0
    deleted_bytes = 0
    kept_files = 0
    error_count = 0

    for dirpath, dirnames, filenames in os.walk(share_dir):
        current_dir = Path(dirpath)

        for name in filenames:
            path = current_dir / name
            total_files += 1

            try:
                if not path.is_file():
                    continue

                st = path.stat()
                link_count = getattr(st, "st_nlink", None)

                if link_count is None:
                    logger.error(f"当前平台无法读取硬链接数量 st_nlink，跳过: {path}")
                    error_count += 1
                    continue

                if link_count <= 1:
                    orphan_files += 1
                    file_size = st.st_size

                    logger.info(f"发现孤儿 share 文件，将删除: {path}, size={file_size}, nlink={link_count}")

                    try:
                        cache_key = get_file_cache_key(path)
                    except Exception:
                        cache_key = str(path)

                    try:
                        path.unlink()
                        deleted_files += 1
                        deleted_bytes += file_size

                        if cache_key in cache_data:
                            cache_data.pop(cache_key, None)
                            logger.info(f"已删除对应缓存: {cache_key}")

                        logger.info(f"已删除孤儿 share 文件: {path}")

                    except Exception as e:
                        logger.error(f"删除孤儿 share 文件失败: {path}, 错误: {e}")
                        error_count += 1
                else:
                    kept_files += 1
                    logger.info(f"保留仍有关联的 share 文件: {path}, nlink={link_count}")

            except Exception as e:
                logger.error(f"检查 share 文件失败: {path}, 错误: {e}")
                error_count += 1

    # 可选：清理 share 目录下的空子目录
    for dirpath, dirnames, filenames in os.walk(share_dir, topdown=False):
        current_dir = Path(dirpath)
        if current_dir == share_dir:
            continue

        try:
            if not any(current_dir.iterdir()):
                current_dir.rmdir()
                logger.info(f"已删除空目录: {current_dir}")
        except Exception as e:
            logger.warning(f"删除空目录失败: {current_dir}, 错误: {e}")

    elapsed = time.time() - start

    logger.info("=" * 80)
    logger.info("CLEAN 模式完成")
    logger.info(f"share 目录: {share_dir}")
    logger.info(f"检查文件数: {total_files}")
    logger.info(f"孤儿文件数: {orphan_files}")
    logger.info(f"已删除文件数: {deleted_files}")
    logger.info(f"保留文件数: {kept_files}")
    logger.info(f"删除释放空间: {deleted_bytes} 字节 ({deleted_bytes / 1024 / 1024 / 1024:.2f} GB)")
    logger.info(f"错误数量: {error_count}")
    logger.info(f"耗时: {elapsed:.2f} 秒")


def parse_size(size_str: str) -> int:
    """
    支持:
      1024
      10KB
      100MB
      2GB
    """
    s = size_str.strip().upper()
    units = {
        "B": 1,
        "KB": 1024,
        "MB": 1024 * 1024,
        "GB": 1024 * 1024 * 1024,
        "TB": 1024 * 1024 * 1024 * 1024,
    }

    for unit in ["TB", "GB", "MB", "KB", "B"]:
        if s.endswith(unit):
            num = s[:-len(unit)].strip()
            return int(float(num) * units[unit])

    return int(s)


def main():
    parser = argparse.ArgumentParser(description="Windows 文件去重并改为硬链接")
    parser.add_argument("root", help="要扫描的根目录")
    parser.add_argument("--min-size", default="1MB", help="只处理大于等于该大小的文件，如 100MB")
    parser.add_argument("--log", default="dedup.log", help="日志文件路径")
    parser.add_argument("--cache-file", default=DEFAULT_CACHE_FILE, help="JSON 缓存文件路径")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="只预演，不实际修改文件")
    mode.add_argument("--execute", action="store_true", help="实际执行文件去重")
    mode.add_argument("--clean", action="store_true", help="清理 share 目录中没有外部硬链接关联的孤儿文件")

    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"扫描目录不存在: {root}")
        sys.exit(1)
    if not root.is_dir():
        print(f"扫描路径不是目录: {root}")
        sys.exit(1)

    min_size = parse_size(args.min_size)
    log_file = Path(args.log)
    cache_file = Path(args.cache_file)
    share_dir = get_share_dir(root)

    logger = setup_logger(log_file)

    logger.info("=" * 80)
    logger.info("启动任务")
    logger.info(f"扫描目录: {root}")
    logger.info(f"自动生成 share 目录: {share_dir}")
    logger.info(f"最小处理文件大小: {min_size} 字节")
    logger.info(f"日志文件: {log_file}")
    logger.info(f"缓存文件: {cache_file}")

    if args.clean:
        logger.info("运行模式: CLEAN")
    elif args.dry_run:
        logger.info("运行模式: DRY-RUN")
    else:
        logger.info("运行模式: EXECUTE")

    cache_data = load_cache(cache_file, logger)

    if args.clean:
        clean_share_dir(share_dir, logger, cache_data)
    else:
        dedup(root, min_size, share_dir, logger, dry_run=args.dry_run, cache_data=cache_data)

    save_cache(cache_file, cache_data, logger)


if __name__ == "__main__":
    main()