import os
import logging
from pathlib import Path
from collections import defaultdict

from mutagen import File
from mutagen.id3 import ID3NoHeaderError
from opencc import OpenCC

# =========================
# 硬编码配置
# =========================
MUSIC_DIR = r"D:\music\flac\CN"
LOG_FILE = "music_convert.log"

MUSIC_EXTENSIONS = {
    ".mp3", ".flac", ".m4a", ".mp4", ".aac", ".ogg", ".opus", ".wav", ".wma"
}

# 繁体转简体
cc = OpenCC("t2s")


# =========================
# 日志配置
# =========================
def setup_logger():
    logger = logging.getLogger("music_converter")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 文件
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


# =========================
# 统计
# =========================
stats = defaultdict(int)


# =========================
# 文本转换
# =========================
def convert_text(text):
    if not isinstance(text, str):
        return text
    return cc.convert(text)


def convert_tag_value(value):
    if isinstance(value, str):
        return convert_text(value)
    elif isinstance(value, list):
        return [convert_tag_value(v) for v in value]
    elif isinstance(value, tuple):
        return tuple(convert_tag_value(list(value)))
    return value


# =========================
# 文件遍历
# =========================
def iter_music_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in MUSIC_EXTENSIONS:
                yield os.path.join(root, file)


# =========================
# Tag 处理
# =========================
def process_tags(file_path):
    stats["tag_checked"] += 1

    try:
        audio = File(file_path, easy=False)
        if audio is None:
            logger.warning(f"[跳过] 无法识别文件: {file_path}")
            stats["tag_skipped_unrecognized"] += 1
            return False

        changed = False

        if hasattr(audio, "tags") and audio.tags:
            tags = audio.tags

            for key in list(tags.keys()):
                try:
                    value = tags[key]

                    # 常见 mutagen frame，通常有 text 属性
                    if hasattr(value, "text"):
                        old_text = list(value.text)
                        new_text = [convert_text(v) if isinstance(v, str) else v for v in value.text]
                        if old_text != new_text:
                            value.text = new_text
                            changed = True
                            logger.info(f"[Tag修改] {file_path} | {key} | {old_text} -> {new_text}")

                    # 字符串列表
                    elif isinstance(value, list):
                        new_value = convert_tag_value(value)
                        if value != new_value:
                            tags[key] = new_value
                            changed = True
                            logger.info(f"[Tag修改] {file_path} | {key} | {value} -> {new_value}")

                    # 单字符串
                    elif isinstance(value, str):
                        new_value = convert_text(value)
                        if value != new_value:
                            tags[key] = new_value
                            changed = True
                            logger.info(f"[Tag修改] {file_path} | {key} | {value} -> {new_value}")

                    # 元组
                    elif isinstance(value, tuple):
                        new_value = convert_tag_value(value)
                        if value != new_value:
                            tags[key] = new_value
                            changed = True
                            logger.info(f"[Tag修改] {file_path} | {key} | {value} -> {new_value}")

                except Exception as e:
                    logger.warning(f"[警告] 处理 tag 项失败: file={file_path}, key={key}, err={e}")
                    stats["tag_item_error"] += 1

            if changed:
                audio.save()
                logger.info(f"[已更新Tag] {file_path}")
                stats["tag_changed"] += 1
                return True
            else:
                logger.info(f"[Tag无变化] {file_path}")
                stats["tag_unchanged"] += 1
                return False
        else:
            logger.info(f"[无Tag] {file_path}")
            stats["tag_no_tag"] += 1
            return False

    except ID3NoHeaderError:
        logger.warning(f"[跳过] 无 ID3 头: {file_path}")
        stats["tag_skipped_no_id3"] += 1
        return False
    except Exception as e:
        logger.error(f"[错误] 处理 tag 失败: {file_path}, err={e}")
        stats["tag_error"] += 1
        return False


# =========================
# 文件名处理
# =========================
def rename_file(file_path):
    stats["filename_checked"] += 1

    path = Path(file_path)
    new_name = convert_text(path.name)

    if new_name == path.name:
        logger.info(f"[文件名无变化] {file_path}")
        stats["filename_unchanged"] += 1
        return str(path)

    new_path = path.with_name(new_name)

    if new_path.exists():
        logger.warning(f"[跳过重命名] 目标已存在: {new_path}")
        stats["filename_conflict"] += 1
        return str(path)

    try:
        path.rename(new_path)
        logger.info(f"[已重命名] {path} -> {new_path}")
        stats["filename_changed"] += 1
        return str(new_path)
    except Exception as e:
        logger.error(f"[错误] 重命名失败: {path}, err={e}")
        stats["filename_error"] += 1
        return str(path)


# =========================
# 统计输出
# =========================
def print_summary():
    summary_lines = [
        "",
        "=" * 50,
        "处理完成，统计结果：",
        "=" * 50,
        f"扫描到音乐文件数         : {stats['files_total']}",
        f"Tag检查文件数            : {stats['tag_checked']}",
        f"Tag成功修改文件数        : {stats['tag_changed']}",
        f"Tag无变化文件数          : {stats['tag_unchanged']}",
        f"无Tag文件数              : {stats['tag_no_tag']}",
        f"无法识别Tag文件数        : {stats['tag_skipped_unrecognized']}",
        f"无ID3头跳过数            : {stats['tag_skipped_no_id3']}",
        f"Tag项处理错误数          : {stats['tag_item_error']}",
        f"Tag整体处理错误数        : {stats['tag_error']}",
        "-" * 50,
        f"文件名检查数             : {stats['filename_checked']}",
        f"文件名成功重命名数       : {stats['filename_changed']}",
        f"文件名无变化数           : {stats['filename_unchanged']}",
        f"文件名冲突跳过数         : {stats['filename_conflict']}",
        f"文件名重命名错误数       : {stats['filename_error']}",
        "=" * 50,
        f"日志文件                 : {Path(LOG_FILE).resolve()}",
        "=" * 50,
    ]

    for line in summary_lines:
        logger.info(line)


# =========================
# 主流程
# =========================
def main():
    logger.info("=" * 50)
    logger.info("开始处理音乐文件")
    logger.info(f"目标目录: {MUSIC_DIR}")
    logger.info("=" * 50)

    if not os.path.isdir(MUSIC_DIR):
        logger.error(f"目录不存在: {MUSIC_DIR}")
        return

    files = list(iter_music_files(MUSIC_DIR))
    stats["files_total"] = len(files)

    logger.info(f"共扫描到 {len(files)} 个音乐文件")

    for index, file_path in enumerate(files, start=1):
        logger.info("-" * 50)
        logger.info(f"[{index}/{len(files)}] 处理文件: {file_path}")

        # 先改 tag
        process_tags(file_path)

        # 再改文件名
        rename_file(file_path)

    print_summary()


if __name__ == "__main__":
    main()
