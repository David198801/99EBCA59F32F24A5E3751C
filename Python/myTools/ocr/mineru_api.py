# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import time
import shutil
import hashlib
import logging
import subprocess
from datetime import datetime

import requests

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("请先安装依赖: pip install PyPDF2 requests")
    sys.exit(1)


# =========================
# 硬编码配置
# =========================
API_TOKEN = ""
ROOT_PDF_DIR = r"E:\BaiduNetdiskDownload"
WORKPLACE_DIR = os.path.abspath("workplace")
PDF_PATHS_TXT = os.path.join(WORKPLACE_DIR, "pdf_paths.txt")
STATUS_JSON = os.path.join(WORKPLACE_DIR, "status.json")
LOG_DIR = os.path.join(WORKPLACE_DIR, "logs")
TMP_DIR = os.path.join(WORKPLACE_DIR, "tmp")
OUTPUT_DIR = os.path.join(WORKPLACE_DIR, "output")
TASKS_DAILY_DIR = WORKPLACE_DIR

# 7z 命令路径（Windows）
SEVEN_Z_EXE = r"C:\Program Files\7-Zip-Zstandard\7z.exe"

# MinerU 接口
APPLY_UPLOAD_URL = "https://mineru.net/api/v4/file-urls/batch"
RESULT_QUERY_URL_TEMPLATE = "https://mineru.net/api/v4/extract-results/batch/{batch_id}"

# 解析参数
MODEL_VERSION = "vlm"
ENABLE_FORMULA = True
ENABLE_TABLE = True
LANGUAGE = "ch"
FILE_IS_OCR = True
EXTRA_FORMATS = []

# 运行参数
MAX_PAGES_PER_TASK = 200
DAILY_MAX_TASKS = 100
UPLOAD_TASK_INTERVAL_SECONDS = 5
POLL_INTERVAL_SECONDS = 300
REQUEST_TIMEOUT = 120
DOWNLOAD_TIMEOUT = 300
RETRY_COUNT = 3
RETRY_SLEEP_SECONDS = 5

POLL_EXISTING_PENDING_TASKS_FIRST = True


# =========================
# 基础工具
# =========================
def ensure_dirs():
    os.makedirs(WORKPLACE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def setup_logger():
    ensure_dirs()
    today = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(LOG_DIR, f"{today}.log")

    logger = logging.getLogger("mineru_runner")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


logger = setup_logger()


def ensure_7z_exists_or_exit():
    if not os.path.exists(SEVEN_Z_EXE):
        logger.error(f"未找到7z命令行程序: {SEVEN_Z_EXE}")
        logger.error("请安装7-Zip并修改脚本中的 SEVEN_Z_EXE 路径后重试。程序退出。")
        sys.exit(1)


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"读取JSON失败: {path}, error={e}")
        return default


def save_json(path, data):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def sanitize_name(name):
    return re.sub(r'[\\/:*?"<>|]+', "_", name)


def calc_file_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            sha1.update(chunk)
    return sha1.hexdigest()


def relpath_under_root(abs_path, root_dir):
    return os.path.relpath(abs_path, root_dir)


def get_today_task_file():
    today = datetime.now().strftime("%Y%m%d")
    return os.path.join(TASKS_DAILY_DIR, f"{today}_task.json")


def load_daily_task_record():
    path = get_today_task_file()
    return load_json(path, {"date": datetime.now().strftime("%Y%m%d"), "submitted_tasks": []})


def save_daily_task_record(data):
    save_json(get_today_task_file(), data)


def current_daily_task_count():
    data = load_daily_task_record()
    return len(data.get("submitted_tasks", []))


def append_daily_task_record(task_info):
    data = load_daily_task_record()
    data.setdefault("submitted_tasks", []).append(task_info)
    save_daily_task_record(data)


def safe_request(method, url, **kwargs):
    for i in range(RETRY_COUNT):
        try:
            resp = requests.request(method, url, **kwargs)
            return resp
        except Exception as e:
            logger.warning(f"请求失败({i+1}/{RETRY_COUNT}) {url}, error={e}")
            if i < RETRY_COUNT - 1:
                time.sleep(RETRY_SLEEP_SECONDS)
    raise RuntimeError(f"请求最终失败: {url}")


# =========================
# PDF 路径缓存
# =========================
def build_pdf_paths_if_needed():
    if os.path.exists(PDF_PATHS_TXT):
        logger.info(f"已存在 {PDF_PATHS_TXT}，跳过重新扫描PDF。")
        return

    logger.info(f"开始递归扫描PDF目录: {ROOT_PDF_DIR}")
    pdf_paths = []
    for root, dirs, files in os.walk(ROOT_PDF_DIR):
        for fn in files:
            if fn.lower().endswith(".pdf"):
                abs_path = os.path.abspath(os.path.join(root, fn))
                pdf_paths.append(abs_path)

    pdf_paths.sort()
    with open(PDF_PATHS_TXT, "w", encoding="utf-8") as f:
        for p in pdf_paths:
            f.write(p + "\n")

    logger.info(f"PDF扫描完成，共 {len(pdf_paths)} 个，已写入 {PDF_PATHS_TXT}")


def load_pdf_paths():
    if not os.path.exists(PDF_PATHS_TXT):
        return []
    with open(PDF_PATHS_TXT, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# =========================
# 状态管理
# =========================
def load_status():
    default = {"files": {}}
    return load_json(STATUS_JSON, default)


def save_status(status):
    save_json(STATUS_JSON, status)


def ensure_file_status(status, pdf_path):
    files = status.setdefault("files", {})
    if pdf_path not in files:
        files[pdf_path] = {
            "completed": False,
            "file_sha1": calc_file_sha1(pdf_path) if os.path.exists(pdf_path) else "",
            "page_count": None,
            "parts": [],
            "output_dir": "",
            "last_update": ""
        }
    return files[pdf_path]


# =========================
# PDF页数与拆分
# =========================
def get_pdf_page_count(pdf_path):
    reader = PdfReader(pdf_path)
    return len(reader.pages)


def split_pdf_to_two_parts(pdf_path, page_count):
    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    file_sha1 = calc_file_sha1(pdf_path)
    task_dir = os.path.join(TMP_DIR, sanitize_name(basename + "_" + file_sha1))
    os.makedirs(task_dir, exist_ok=True)

    part1_path = os.path.join(task_dir, f"{basename}_part1.pdf")
    part2_path = os.path.join(task_dir, f"{basename}_part2.pdf")

    if not os.path.exists(part1_path) or not os.path.exists(part2_path):
        reader = PdfReader(pdf_path)

        writer1 = PdfWriter()
        for i in range(0, min(MAX_PAGES_PER_TASK, page_count)):
            writer1.add_page(reader.pages[i])
        with open(part1_path, "wb") as f:
            writer1.write(f)

        writer2 = PdfWriter()
        for i in range(MAX_PAGES_PER_TASK, page_count):
            writer2.add_page(reader.pages[i])
        with open(part2_path, "wb") as f:
            writer2.write(f)

    return [
        {
            "part_no": 1,
            "page_range": f"1-{MAX_PAGES_PER_TASK}",
            "upload_file_path": part1_path
        },
        {
            "part_no": 2,
            "page_range": f"{MAX_PAGES_PER_TASK + 1}-{page_count}",
            "upload_file_path": part2_path
        }
    ]


def create_tasks_for_pdf(pdf_path, status):
    fs = ensure_file_status(status, pdf_path)
    if fs.get("page_count") is None:
        fs["page_count"] = get_pdf_page_count(pdf_path)
        fs["last_update"] = datetime.now().isoformat()
        save_status(status)

    page_count = fs["page_count"]

    if page_count <= MAX_PAGES_PER_TASK:
        return [{
            "part_no": 1,
            "page_range": f"1-{page_count}",
            "upload_file_path": pdf_path
        }]
    else:
        return split_pdf_to_two_parts(pdf_path, page_count)


# =========================
# 接口调用
# =========================
def apply_upload_url_for_single_task(upload_filename, data_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    data = {
        "files": [
            {
                "name": upload_filename,
                "data_id": data_id,
                "is_ocr": FILE_IS_OCR
            }
        ],
        "model_version": MODEL_VERSION,
        "enable_formula": ENABLE_FORMULA,
        "enable_table": ENABLE_TABLE,
        "language": LANGUAGE
    }

    if EXTRA_FORMATS:
        data["extra_formats"] = EXTRA_FORMATS

    resp = safe_request(
        "POST",
        APPLY_UPLOAD_URL,
        headers=headers,
        json=data,
        timeout=REQUEST_TIMEOUT
    )

    if resp.status_code != 200:
        raise RuntimeError(f"申请上传链接失败，HTTP={resp.status_code}, body={resp.text}")

    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"申请上传链接失败，code={result.get('code')}, msg={result.get('msg')}")

    batch_id = result["data"]["batch_id"]
    urls = result["data"]["file_urls"]
    if not urls:
        raise RuntimeError("未返回上传URL")

    return batch_id, urls[0], result


def upload_file_to_url(upload_url, local_file_path):
    with open(local_file_path, "rb") as f:
        resp = safe_request(
            "PUT",
            upload_url,
            data=f,
            timeout=REQUEST_TIMEOUT
        )
    if resp.status_code != 200:
        raise RuntimeError(f"上传失败，HTTP={resp.status_code}, body={resp.text}")


def query_batch_result(batch_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = RESULT_QUERY_URL_TEMPLATE.format(batch_id=batch_id)
    resp = safe_request(
        "GET",
        url,
        headers=headers,
        timeout=REQUEST_TIMEOUT
    )
    if resp.status_code != 200:
        raise RuntimeError(f"查询结果失败，HTTP={resp.status_code}, body={resp.text}")

    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"查询结果失败，code={result.get('code')}, msg={result.get('msg')}")
    return result


def download_file(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with requests.get(url, stream=True, timeout=DOWNLOAD_TIMEOUT) as r:
        if r.status_code != 200:
            raise RuntimeError(f"下载失败，HTTP={r.status_code}, url={url}")
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


# =========================
# 输出路径
# =========================
def get_pdf_output_base_dir(pdf_path):
    rel_path = relpath_under_root(pdf_path, ROOT_PDF_DIR)
    rel_dir = os.path.dirname(rel_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return os.path.join(OUTPUT_DIR, rel_dir, pdf_name)


def get_zip_save_path(pdf_path, part_no, batch_id):
    base_dir = get_pdf_output_base_dir(pdf_path)
    os.makedirs(base_dir, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    zip_name = f"{pdf_name}_part{part_no}_{batch_id}.zip"
    return os.path.join(base_dir, zip_name)


# =========================
# 解压与合并
# =========================
def extract_zip_with_7z(zip_path, dest_dir):
    if not os.path.exists(SEVEN_Z_EXE):
        raise RuntimeError(f"7z不存在: {SEVEN_Z_EXE}")
    os.makedirs(dest_dir, exist_ok=True)
    cmd = [SEVEN_Z_EXE, "x", "-y", f"-o{dest_dir}", zip_path]
    logger.info(f"执行解压命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"7z解压失败: {result.stderr}\n{result.stdout}")


def find_all_md_files(root_dir):
    result = []
    for root, dirs, files in os.walk(root_dir):
        for fn in files:
            if fn.lower().endswith(".md"):
                result.append(os.path.join(root, fn))
    return result


def pick_preferred_md(root_dir):
    """
    优先选择 full.md
    如果没有，则退化为该目录下找到的第一个 md
    """
    full_md_candidates = []
    all_md_files = []

    for root, dirs, files in os.walk(root_dir):
        for fn in files:
            if fn.lower().endswith(".md"):
                full_path = os.path.join(root, fn)
                all_md_files.append(full_path)
                if fn.lower() == "full.md":
                    full_md_candidates.append(full_path)

    if full_md_candidates:
        full_md_candidates.sort()
        return full_md_candidates[0]

    if all_md_files:
        all_md_files.sort()
        return all_md_files[0]

    return None


def merge_images_dirs(src_dir, target_images_dir):
    for root, dirs, files in os.walk(src_dir):
        if os.path.basename(root).lower() == "images":
            os.makedirs(target_images_dir, exist_ok=True)
            for fn in files:
                src = os.path.join(root, fn)
                dst = os.path.join(target_images_dir, fn)
                if os.path.exists(dst):
                    name, ext = os.path.splitext(fn)
                    idx = 1
                    while True:
                        new_name = f"{name}_{idx}{ext}"
                        new_dst = os.path.join(target_images_dir, new_name)
                        if not os.path.exists(new_dst):
                            dst = new_dst
                            break
                        idx += 1
                shutil.move(src, dst)


def merge_md_files_in_part_order(ordered_md_files, merged_md_path):
    with open(merged_md_path, "w", encoding="utf-8") as out:
        first_written = False
        for md in ordered_md_files:
            if not md or not os.path.exists(md):
                continue
            with open(md, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().strip()
            if not content:
                continue
            if first_written:
                out.write("\n\n\n\n")
            out.write(content)
            first_written = True
    logger.info(f"已按part顺序合并MD到: {merged_md_path}")


def process_completed_pdf_outputs(pdf_path, status):
    fs = ensure_file_status(status, pdf_path)
    parts = fs.get("parts", [])
    if not parts:
        return

    for part in parts:
        if part.get("state") != "done" or not part.get("zip_local_path") or not os.path.exists(part.get("zip_local_path")):
            logger.info(f"文件尚未全部完成，不处理输出: {pdf_path}")
            return

    pdf_output_dir = get_pdf_output_base_dir(pdf_path)
    os.makedirs(pdf_output_dir, exist_ok=True)

    # 关键修改：按 part_no 排序
    ordered_parts = sorted(parts, key=lambda x: x.get("part_no", 999999))

    extracted_part_dirs = []
    for part in ordered_parts:
        zip_path = part["zip_local_path"]
        zip_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_dir = os.path.join(pdf_output_dir, zip_name)
        if not os.path.exists(extract_dir):
            extract_zip_with_7z(zip_path, extract_dir)
        extracted_part_dirs.append((part["part_no"], extract_dir))

    if len(parts) == 1:
        logger.info(f"单任务文件已解压完成: {pdf_path}")
        fs["completed"] = True
        fs["last_update"] = datetime.now().isoformat()
        save_status(status)
        return

    merged_md_path = os.path.join(pdf_output_dir, "full_merged.md")
    target_images_dir = os.path.join(pdf_output_dir, "images")

    ordered_md_files = []
    for part_no, extract_dir in extracted_part_dirs:
        md_file = pick_preferred_md(extract_dir)
        if md_file:
            ordered_md_files.append(md_file)
            logger.info(f"part{part_no} 选中MD文件: {md_file}")
        else:
            logger.warning(f"part{part_no} 未找到MD文件: {extract_dir}")
        merge_images_dirs(extract_dir, target_images_dir)

    merge_md_files_in_part_order(ordered_md_files, merged_md_path)

    for _, ed in extracted_part_dirs:
        if os.path.exists(ed):
            shutil.rmtree(ed, ignore_errors=True)
            logger.info(f"已删除临时解压目录: {ed}")

    fs["completed"] = True
    fs["last_update"] = datetime.now().isoformat()
    save_status(status)
    logger.info(f"多part文件合并完成: {pdf_path}")


# =========================
# 任务状态处理
# =========================
def submit_task_for_pdf_part(pdf_path, part_task, status):
    fs = ensure_file_status(status, pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    part_no = part_task["part_no"]
    upload_file_path = part_task["upload_file_path"]
    page_range = part_task["page_range"]
    file_sha1 = fs["file_sha1"]

    for p in fs["parts"]:
        if p.get("part_no") == part_no and p.get("state") == "done":
            logger.info(f"已完成，跳过提交: {pdf_path} part{part_no}")
            return

    for p in fs["parts"]:
        if p.get("part_no") == part_no and p.get("state") in ("waiting-file", "pending", "running", "converting", "uploaded"):
            logger.info(f"已提交未完成，跳过重复提交: {pdf_path} part{part_no}")
            return

    daily_count = current_daily_task_count()
    if daily_count >= DAILY_MAX_TASKS:
        logger.warning(f"今日已提交 {DAILY_MAX_TASKS} 个任务，不再继续提交。")
        raise RuntimeError("DAILY_TASK_LIMIT_REACHED")

    upload_filename = os.path.basename(upload_file_path)
    data_id = f"{sanitize_name(pdf_name)}_part{part_no}_{file_sha1[:12]}"

    logger.info(f"开始申请上传链接: {pdf_path} part{part_no}, file={upload_filename}, data_id={data_id}")
    batch_id, upload_url, raw_resp = apply_upload_url_for_single_task(upload_filename, data_id)

    logger.info(f"开始上传文件: {upload_file_path}")
    upload_file_to_url(upload_url, upload_file_path)
    logger.info(f"上传完成: {pdf_path} part{part_no}, batch_id={batch_id}")

    found = False
    for p in fs["parts"]:
        if p.get("part_no") == part_no:
            p.update({
                "part_no": part_no,
                "page_range": page_range,
                "upload_file_path": upload_file_path,
                "batch_id": batch_id,
                "data_id": data_id,
                "state": "uploaded",
                "zip_url": "",
                "zip_local_path": "",
                "err_msg": "",
                "last_query": "",
                "submitted_at": datetime.now().isoformat()
            })
            found = True
            break

    if not found:
        fs["parts"].append({
            "part_no": part_no,
            "page_range": page_range,
            "upload_file_path": upload_file_path,
            "batch_id": batch_id,
            "data_id": data_id,
            "state": "uploaded",
            "zip_url": "",
            "zip_local_path": "",
            "err_msg": "",
            "last_query": "",
            "submitted_at": datetime.now().isoformat()
        })

    fs["output_dir"] = get_pdf_output_base_dir(pdf_path)
    fs["last_update"] = datetime.now().isoformat()
    save_status(status)

    append_daily_task_record({
        "pdf_path": pdf_path,
        "part_no": part_no,
        "batch_id": batch_id,
        "data_id": data_id,
        "submitted_at": datetime.now().isoformat()
    })

    logger.info(f"提交任务记录完成，今日累计任务数: {current_daily_task_count()}")
    logger.info(f"按要求暂停 {UPLOAD_TASK_INTERVAL_SECONDS} 秒")
    time.sleep(UPLOAD_TASK_INTERVAL_SECONDS)


def poll_once_for_all_pending(status):
    files = status.get("files", {})
    changed = False

    for pdf_path, fs in files.items():
        if fs.get("completed"):
            continue

        parts = fs.get("parts", [])
        for part in parts:
            state = part.get("state", "")
            if state == "done" and part.get("zip_local_path") and os.path.exists(part.get("zip_local_path")):
                continue
            if state == "failed":
                continue
            if not part.get("batch_id"):
                continue

            batch_id = part["batch_id"]
            logger.info(f"查询状态: {pdf_path} part{part.get('part_no')} batch_id={batch_id}")
            try:
                result = query_batch_result(batch_id)
                extract_result_list = result["data"].get("extract_result", [])
                if not extract_result_list:
                    logger.warning(f"未返回extract_result: batch_id={batch_id}")
                    continue

                item = extract_result_list[0]
                new_state = item.get("state", "")
                part["state"] = new_state
                part["err_msg"] = item.get("err_msg", "")
                part["last_query"] = datetime.now().isoformat()
                changed = True

                if new_state == "done":
                    zip_url = item.get("full_zip_url", "")
                    if zip_url:
                        part["zip_url"] = zip_url
                        zip_local_path = get_zip_save_path(pdf_path, part["part_no"], batch_id)
                        if not os.path.exists(zip_local_path):
                            logger.info(f"开始下载结果zip: {zip_url}")
                            download_file(zip_url, zip_local_path)
                            logger.info(f"下载完成: {zip_local_path}")
                        part["zip_local_path"] = zip_local_path
                    else:
                        logger.warning(f"done但没有full_zip_url: batch_id={batch_id}")

                elif new_state == "failed":
                    logger.error(f"任务失败: {pdf_path} part{part.get('part_no')}, err={part['err_msg']}")
                else:
                    logger.info(f"任务未完成: {pdf_path} part{part.get('part_no')}, state={new_state}")

            except Exception as e:
                logger.error(f"轮询任务异常: {pdf_path} part{part.get('part_no')}, error={e}")

        parts = fs.get("parts", [])
        if parts and all(p.get("state") == "done" and p.get("zip_local_path") for p in parts):
            try:
                process_completed_pdf_outputs(pdf_path, status)
                changed = True
            except Exception as e:
                logger.error(f"处理输出失败: {pdf_path}, error={e}")

    if changed:
        save_status(status)


def has_pending_tasks(status):
    files = status.get("files", {})
    for pdf_path, fs in files.items():
        if fs.get("completed"):
            continue
        for p in fs.get("parts", []):
            if p.get("state") in ("uploaded", "waiting-file", "pending", "running", "converting", ""):
                return True
    return False


# =========================
# 主流程
# =========================
def main():
    ensure_dirs()
    ensure_7z_exists_or_exit()

    logger.info("程序启动")
    logger.info(f"WORKPLACE_DIR = {WORKPLACE_DIR}")
    logger.info(f"ROOT_PDF_DIR = {ROOT_PDF_DIR}")

    build_pdf_paths_if_needed()
    pdf_paths = load_pdf_paths()
    logger.info(f"已加载PDF路径数: {len(pdf_paths)}")

    status = load_status()

    if POLL_EXISTING_PENDING_TASKS_FIRST:
        logger.info("先轮询已有未完成任务一次")
        poll_once_for_all_pending(status)
        status = load_status()

    daily_count = current_daily_task_count()
    if daily_count >= DAILY_MAX_TASKS:
        logger.warning(f"今日已经提交 {daily_count} 个任务，达到上限 {DAILY_MAX_TASKS}。")
    else:
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                logger.warning(f"文件不存在，跳过: {pdf_path}")
                continue

            fs = ensure_file_status(status, pdf_path)
            if fs.get("completed"):
                logger.info(f"文件已完成，跳过: {pdf_path}")
                continue

            try:
                tasks = create_tasks_for_pdf(pdf_path, status)
                for task in tasks:
                    if current_daily_task_count() >= DAILY_MAX_TASKS:
                        logger.warning(f"今日已提交满 {DAILY_MAX_TASKS} 个任务，停止新提交。")
                        break
                    submit_task_for_pdf_part(pdf_path, task, status)
                    status = load_status()
            except RuntimeError as e:
                if str(e) == "DAILY_TASK_LIMIT_REACHED":
                    logger.warning("达到当天任务上限，停止提交新任务。")
                    break
                else:
                    logger.error(f"提交任务失败: {pdf_path}, error={e}")
            except Exception as e:
                logger.error(f"处理PDF失败: {pdf_path}, error={e}")

            if current_daily_task_count() >= DAILY_MAX_TASKS:
                break

    logger.info("进入轮询阶段，每5分钟检查一次状态。")
    while True:
        status = load_status()
        if not has_pending_tasks(status):
            logger.info("没有待处理任务，程序结束。")
            break

        poll_once_for_all_pending(status)
        logger.info(f"等待 {POLL_INTERVAL_SECONDS} 秒后继续轮询。")
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()