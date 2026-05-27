# coding:utf8
import os
import json
import shutil
import traceback
import subprocess
import multiprocessing
import logging
from multiprocessing.pool import ThreadPool

from mutagen import File as MutagenFile
from mutagen.flac import FLAC, Picture
from mutagen.mp4 import MP4, MP4Cover, MP4FreeForm
from mutagen.id3 import ID3, APIC, USLT, COMM
from mutagen.apev2 import APEv2File

musicPath = r"D:\temp"
qaacPath = r"qaac64.exe"
outFormat = "m4a"
setBitrate = "256k"

flacDirPath = os.path.join(musicPath, "flac")
outDirPath = os.path.join(musicPath, "qaac" + setBitrate)

if not os.path.exists(outDirPath):
    os.makedirs(outDirPath)

# ----------------------------
# 日志配置
# ----------------------------
log_dir = os.path.join(musicPath, "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "convert.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Script started")
logger.info("musicPath=%s", musicPath)
logger.info("flacDirPath=%s", flacDirPath)
logger.info("outDirPath=%s", outDirPath)
logger.info("qaacPath=%s, outFormat=%s, setBitrate=%s", qaacPath, outFormat, setBitrate)


# ----------------------------
# 基础工具
# ----------------------------
def run_cmd(cmd, capture_output=False):
    logger.debug("Run command: %s", cmd)
    if capture_output:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        if result.returncode != 0:
            logger.warning("Command failed(returncode=%s): %s", result.returncode, cmd)
            if result.stderr:
                logger.warning("stderr: %s", result.stderr.strip())
        return result
    return subprocess.call(cmd, shell=False)


def ensure_parent_dir(path):
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
        logger.debug("Created parent dir: %s", parent)


def safe_remove(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            logger.debug("Removed temp file: %s", path)
        except Exception as e:
            logger.exception("Delete failed: %s, error=%s", path, e)


def get_media_info(file_path):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    result = run_cmd(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("ffprobe failed: {}\n{}".format(file_path, result.stderr))
    return json.loads(result.stdout)


def get_bitrate(info):
    bit_rate = info.get("format", {}).get("bit_rate")
    if bit_rate:
        return int(int(bit_rate) / 1000)

    for stream in info.get("streams", []):
        if stream.get("codec_type") == "audio":
            stream_br = stream.get("bit_rate")
            if stream_br:
                return int(int(stream_br) / 1000)
    return 0


def get_sample_rate(info):
    for stream in info.get("streams", []):
        if stream.get("codec_type") == "audio":
            sr = stream.get("sample_rate")
            if sr:
                return str(sr)
    return ""


def choose_bitrate(n):
    max_bitrate = int(setBitrate[:-1])
    if n >= max_bitrate:
        return max_bitrate

    bitrate_list = [64, 96, 128, 192, 256, 320]
    bitrate_list = [x for x in bitrate_list if x <= max_bitrate]

    for i in bitrate_list:
        if n <= i:
            return i
    return max_bitrate


def build_resample_args(sample_rate):
    if sample_rate == "88200":
        return ["-ar", "44100"]
    elif sample_rate == "96000":
        return ["-ar", "48000"]
    return []


def normalize_text_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def first_or_none(v):
    if isinstance(v, list):
        return v[0] if v else None
    return v


# ----------------------------
# Tag 读取
# ----------------------------
def extract_tags_and_artwork(src_path):
    """
    从源文件读取尽可能完整的标签、封面、歌词
    返回:
    {
        "text_tags": dict,
        "lyrics": [str, ...],
        "comment": [str, ...],
        "artworks": [{"data": bytes, "mime": str, "type": int, "desc": str}, ...]
    }
    """
    result = {
        "text_tags": {},
        "lyrics": [],
        "comment": [],
        "artworks": []
    }

    audio = MutagenFile(src_path)
    if audio is None:
        logger.warning("Mutagen cannot open file: %s", src_path)
        return result

    ext = os.path.splitext(src_path)[1].lower()

    try:
        # ---------------- FLAC ----------------
        if isinstance(audio, FLAC):
            for k, v in audio.tags.items():
                lk = k.lower()
                vals = normalize_text_list(v)
                if not vals:
                    continue

                if lk in ("lyrics", "unsyncedlyrics", "unsynchronizedlyrics"):
                    result["lyrics"].extend(vals)
                elif lk in ("comment", "description"):
                    result["comment"].extend(vals)
                else:
                    result["text_tags"][lk] = vals

            for pic in audio.pictures:
                result["artworks"].append({
                    "data": pic.data,
                    "mime": pic.mime or "image/jpeg",
                    "type": getattr(pic, "type", 3),
                    "desc": getattr(pic, "desc", "") or ""
                })

        # ---------------- MP4/M4A ----------------
        elif isinstance(audio, MP4):
            for k, v in audio.tags.items():
                if k == "covr":
                    for cover in v:
                        imageformat = getattr(cover, "imageformat", MP4Cover.FORMAT_JPEG)
                        mime = "image/png" if imageformat == MP4Cover.FORMAT_PNG else "image/jpeg"
                        result["artworks"].append({
                            "data": bytes(cover),
                            "mime": mime,
                            "type": 3,
                            "desc": ""
                        })
                elif k == "\xa9lyr":
                    result["lyrics"].extend(normalize_text_list(v))
                elif k == "----:com.apple.iTunes:LYRICS":
                    vals = []
                    for item in v:
                        if isinstance(item, bytes):
                            vals.append(item.decode("utf-8", errors="ignore"))
                        else:
                            vals.append(str(item))
                    result["lyrics"].extend(normalize_text_list(vals))
                else:
                    result["text_tags"][k] = normalize_text_list(v)

        # ---------------- MP3 / ID3 ----------------
        elif hasattr(audio, "tags") and isinstance(audio.tags, ID3):
            id3 = audio.tags

            text_map = {
                "TIT2": "title",
                "TPE1": "artist",
                "TPE2": "albumartist",
                "TALB": "album",
                "TCON": "genre",
                "TDRC": "date",
                "TYER": "date",
                "TRCK": "tracknumber",
                "TPOS": "discnumber",
                "TCOM": "composer",
                "TEXT": "lyricist",
                "TSRC": "isrc",
                "TCOP": "copyright",
                "TPUB": "label",
                "TENC": "encodedby"
            }

            for frame in id3.values():
                frame_id = frame.FrameID

                if frame_id in text_map:
                    vals = []
                    if hasattr(frame, "text"):
                        vals = normalize_text_list(frame.text)
                    if vals:
                        result["text_tags"][text_map[frame_id]] = vals

                elif frame_id == "USLT":
                    if getattr(frame, "text", None):
                        result["lyrics"].append(str(frame.text))

                elif frame_id == "COMM":
                    if getattr(frame, "text", None):
                        if isinstance(frame.text, list):
                            result["comment"].extend(normalize_text_list(frame.text))
                        else:
                            result["comment"].append(str(frame.text))

                elif frame_id == "APIC":
                    result["artworks"].append({
                        "data": frame.data,
                        "mime": frame.mime or "image/jpeg",
                        "type": getattr(frame, "type", 3),
                        "desc": getattr(frame, "desc", "") or ""
                    })

        # ---------------- APE ----------------
        elif isinstance(audio, APEv2File):
            if audio.tags:
                for k, v in audio.tags.items():
                    lk = k.lower()

                    # APE 封面可能是 binary，mutagen 表现不完全统一，这里先只抓文本
                    if lk in ("lyrics", "unsyncedlyrics", "lyric"):
                        result["lyrics"].extend(normalize_text_list(v))
                    elif lk in ("comment", "description"):
                        result["comment"].extend(normalize_text_list(v))
                    else:
                        result["text_tags"][lk] = normalize_text_list(v)

        # ---------------- 其他 Vorbis 类 ----------------
        elif hasattr(audio, "tags") and audio.tags:
            for k, v in audio.tags.items():
                lk = str(k).lower()
                vals = normalize_text_list(v)
                if not vals:
                    continue

                if lk in ("lyrics", "unsyncedlyrics", "unsynchronizedlyrics", "lyric"):
                    result["lyrics"].extend(vals)
                elif lk in ("comment", "description"):
                    result["comment"].extend(vals)
                else:
                    result["text_tags"][lk] = vals

    except Exception:
        logger.exception("Read tag failed: %s", src_path)

    return result


# ----------------------------
# Tag 写入 M4A
# ----------------------------
def set_mp4_text(tags, key, values):
    if not values:
        return
    tags[key] = [str(v) for v in values if str(v).strip()]


def parse_pair_num(text):
    """
    "3/12" -> [(3, 12)]
    "3" -> [(3, 0)]
    """
    if text is None:
        return None
    text = str(text).strip()
    if not text:
        return None

    if "/" in text:
        a, b = text.split("/", 1)
        try:
            return [(int(a.strip() or 0), int(b.strip() or 0))]
        except Exception:
            return None
    else:
        try:
            return [(int(text), 0)]
        except Exception:
            return None


def apply_tags_to_m4a(dst_m4a_path, tag_data):
    """
    使用 mutagen 把标签写入 m4a
    """
    audio = MP4(dst_m4a_path)
    audio.clear()

    src_tags = tag_data.get("text_tags", {})
    lyrics_list = [x for x in tag_data.get("lyrics", []) if str(x).strip()]
    comment_list = [x for x in tag_data.get("comment", []) if str(x).strip()]
    artworks = tag_data.get("artworks", [])

    mapping = {
        "title": "\xa9nam",
        "\xa9nam": "\xa9nam",

        "album": "\xa9alb",
        "\xa9alb": "\xa9alb",

        "artist": "\xa9ART",
        "\xa9art": "\xa9ART",
        "\xa9ART": "\xa9ART",

        "albumartist": "aART",
        "album artist": "aART",
        "aart": "aART",
        "aART": "aART",

        "genre": "\xa9gen",
        "\xa9gen": "\xa9gen",

        "date": "\xa9day",
        "year": "\xa9day",
        "\xa9day": "\xa9day",

        "composer": "\xa9wrt",
        "\xa9wrt": "\xa9wrt",

        "comment": "\xa9cmt",
        "\xa9cmt": "\xa9cmt",

        "description": "\xa9des",
        "\xa9des": "\xa9des",

        "grouping": "\xa9grp",
        "\xa9grp": "\xa9grp",

        "copyright": "cprt",
        "cprt": "cprt",

        "encoder": "\xa9too",
        "encodedby": "\xa9too",
        "\xa9too": "\xa9too",

        "lyrics": "\xa9lyr",
        "\xa9lyr": "\xa9lyr",

        "isrc": "----:com.apple.iTunes:ISRC",
        "label": "----:com.apple.iTunes:LABEL",
        "publisher": "----:com.apple.iTunes:LABEL",
        "catalognumber": "----:com.apple.iTunes:CATALOGNUMBER",
        "barcode": "----:com.apple.iTunes:BARCODE",
        "upc": "----:com.apple.iTunes:BARCODE",
        "media": "----:com.apple.iTunes:MEDIA",
        "albumartistsort": "soaa",
        "albumsort": "soal",
        "artistsort": "soar",
        "titlesort": "sonm",
        "composersort": "soco"
    }

    used_keys = set()

    for src_key, values in src_tags.items():
        lk = str(src_key).strip().lower()
        mp4_key = mapping.get(src_key, None) or mapping.get(lk, None)
        if mp4_key:
            used_keys.add(src_key)
            used_keys.add(lk)

            if mp4_key.startswith("----:com.apple.iTunes:"):
                audio.tags[mp4_key] = [str(v).encode("utf-8") for v in values if str(v).strip()]
            else:
                set_mp4_text(audio.tags, mp4_key, values)

    track_val = None
    disc_val = None

    for key in ("tracknumber", "track", "trkn"):
        if key in src_tags:
            track_val = first_or_none(src_tags[key])
            break
        if key.lower() in src_tags:
            track_val = first_or_none(src_tags[key.lower()])
            break

    for key in ("discnumber", "disc", "disk", "disknumber", "tmpo", "disktotal", "disctotal", "disk#", "disc#"):
        if key in src_tags:
            disc_val = first_or_none(src_tags[key])
            break
        if key.lower() in src_tags:
            disc_val = first_or_none(src_tags[key.lower()])
            break

    if track_val:
        parsed = parse_pair_num(track_val)
        if parsed:
            audio.tags["trkn"] = parsed

    if disc_val:
        parsed = parse_pair_num(disc_val)
        if parsed:
            audio.tags["disk"] = parsed

    if comment_list:
        set_mp4_text(audio.tags, "\xa9cmt", comment_list)

    if lyrics_list:
        set_mp4_text(audio.tags, "\xa9lyr", lyrics_list)
        audio.tags["----:com.apple.iTunes:LYRICS"] = [
            str(v).encode("utf-8") for v in lyrics_list if str(v).strip()
        ]

    if artworks:
        covr = []
        for art in artworks:
            data = art.get("data")
            mime = (art.get("mime") or "").lower()
            if not data:
                continue

            if "png" in mime:
                fmt = MP4Cover.FORMAT_PNG
            else:
                fmt = MP4Cover.FORMAT_JPEG

            covr.append(MP4Cover(data, imageformat=fmt))

        if covr:
            audio.tags["covr"] = covr

    audio.save()
    logger.info("Tags saved: %s", dst_m4a_path)


# ----------------------------
# 任务函数
# ----------------------------
def copy_worker(task):
    src, dst = task
    try:
        shutil.copy2(src, dst)
        logger.info("Copied: %s -> %s", src, dst)
        return 1
    except Exception:
        logger.exception("Copy failed: %s -> %s", src, dst)
        return 0


def cmd_worker(cmd):
    try:
        logger.info("Executing command: %s", " ".join(cmd))
        ret = subprocess.call(cmd, shell=False)
        if ret != 0:
            logger.error("Command failed(ret=%s): %s", ret, cmd)
            return 0
        logger.info("Command success: %s", " ".join(cmd))
        return 1
    except Exception:
        logger.exception("Command exception: %s", cmd)
        return 0


def call_pool(task_list, thread_num, worker_func, task_name="task"):
    if not task_list:
        logger.info("No %s to run", task_name)
        return

    logger.info("Start %s: count=%d, threads=%d", task_name, len(task_list), thread_num)

    pool = ThreadPool(thread_num)
    results = []
    for task in task_list:
        results.append(pool.apply_async(worker_func, (task,)))
    pool.close()
    pool.join()

    success = 0
    for r in results:
        try:
            success += r.get()
        except Exception:
            logger.exception("Get async result failed for %s", task_name)

    logger.info("%s done: %d/%d", task_name, success, len(task_list))


# ----------------------------
# 扫描与生成任务
# ----------------------------
copy_tasks = []
wav_tasks = []
qaac_tasks = []

tag_jobs = []

wav_temp_paths = []
m4a_temp_paths = []

logger.info("Start scanning source directory: %s", flacDirPath)

for root, dirs, files in os.walk(flacDirPath):
    for f in files:
        src_file_path = os.path.join(root, f)
        file_ext = os.path.splitext(f)[1].lower().lstrip(".")

        rel_path = os.path.relpath(src_file_path, flacDirPath)
        out_file_path = os.path.join(outDirPath, rel_path)
        out_file_path = os.path.splitext(out_file_path)[0] + "." + outFormat

        ensure_parent_dir(out_file_path)

        if os.path.exists(out_file_path):
            logger.info("Skip existing file: %s", out_file_path)
            continue

        logger.info("Processing: %s", src_file_path)

        try:
            media_info = get_media_info(src_file_path)
        except Exception as e:
            logger.exception("Skip ffprobe error: %s, error=%s", src_file_path, e)
            continue

        sample_rate = get_sample_rate(media_info)
        extra_args = build_resample_args(sample_rate)
        out_bitrate = setBitrate

        if file_ext == outFormat:
            bitrate = get_bitrate(media_info)
            if bitrate and bitrate < int(setBitrate[:-1]):
                logger.info("Add copy task: src=%s, bitrate=%sk, dst=%s", src_file_path, bitrate, out_file_path)
                copy_tasks.append((src_file_path, out_file_path))
                continue

        if file_ext != "flac":
            bitrate = get_bitrate(media_info)
            if bitrate > 0:
                out_bitrate = str(choose_bitrate(bitrate)) + "k"

        wav_path = out_file_path + ".temp.wav"
        m4a_temp_path = out_file_path + ".temp.m4a"

        wav_cmd = [
            "ffmpeg",
            "-y",
            "-i", src_file_path,
            "-vn"
        ] + extra_args + [wav_path]

        qaac_cmd = [
            qaacPath,
            wav_path,
            "--ignorelength",
            "--threading",
            "-c", out_bitrate[:-1],
            "-o", m4a_temp_path
        ]

        logger.info("Add wav task: %s", wav_cmd)
        logger.info("Add qaac task: %s", qaac_cmd)

        wav_tasks.append(wav_cmd)
        qaac_tasks.append(qaac_cmd)
        wav_temp_paths.append(wav_path)
        m4a_temp_paths.append(m4a_temp_path)

        tag_jobs.append({
            "src": src_file_path,
            "temp_m4a": m4a_temp_path,
            "final_m4a": out_file_path
        })

logger.info("Scan completed: copy_tasks=%d, wav_tasks=%d, qaac_tasks=%d, tag_jobs=%d",
            len(copy_tasks), len(wav_tasks), len(qaac_tasks), len(tag_jobs))


# ----------------------------
# 执行流程
# ----------------------------
call_pool(copy_tasks, 2, copy_worker, "copy")
call_pool(wav_tasks, 2, cmd_worker, "wav")
call_pool(qaac_tasks, multiprocessing.cpu_count(), cmd_worker, "qaac")


# ----------------------------
# 标签写入阶段
# ----------------------------
logger.info("Start tag import stage")

for job in tag_jobs:
    src = job["src"]
    temp_m4a = job["temp_m4a"]
    final_m4a = job["final_m4a"]

    if not os.path.exists(temp_m4a):
        logger.warning("Skip tag import, temp m4a not exists: %s", temp_m4a)
        continue

    try:
        tag_data = extract_tags_and_artwork(src)
        shutil.copy2(temp_m4a, final_m4a)
        apply_tags_to_m4a(final_m4a, tag_data)
        logger.info("Tag imported: %s", final_m4a)
    except Exception:
        logger.exception("Tag import failed: %s -> %s", src, final_m4a)
        try:
            if not os.path.exists(final_m4a):
                shutil.copy2(temp_m4a, final_m4a)
                logger.warning("Fallback copied temp file to final: %s", final_m4a)
        except Exception:
            logger.exception("Fallback copy failed: %s -> %s", temp_m4a, final_m4a)


# ----------------------------
# 删除临时文件
# ----------------------------
logger.info("Start cleaning temp files")

for p in wav_temp_paths:
    safe_remove(p)

for p in m4a_temp_paths:
    safe_remove(p)

logger.info("All done.")