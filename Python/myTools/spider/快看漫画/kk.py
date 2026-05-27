# -*- coding: utf-8 -*-
import os
import re
import json
import time
import logging
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


# =========================
# 配置项
# =========================
INPUT_FILE = "快看漫画.txt"
OUTPUT_ROOT = "downloads"
CHROME_DRIVER_PATH = "d:\cmd\chromedriver.exe"   # 如不在 PATH，改成完整路径
HEADLESS = False                      # 需要手动登录，这里必须 False

PAUSE_SECONDS = 3                      # 每章节处理后暂停秒数
NUXT_WAIT_TIMEOUT = 20                 # 等待 window.__NUXT__ 超时秒数
PAGE_READY_RETRY = 2                   # 页面数据提取失败后的重试次数

REQUEST_TIMEOUT = 30
DOWNLOAD_RETRY_TIMES = 3               # 图片下载失败重试次数
DOWNLOAD_RETRY_SLEEP = 2               # 每次重试间隔秒数

SKIP_IF_CHAPTER_DONE = True
CHAPTER_CACHE_FILENAME = "chapters.json"
LOG_FILE = "kuaikan_spider.log"


# =========================
# 全局运行状态
# =========================
LOGIN_CONFIRMED_THIS_RUN = False


# =========================
# 日志配置
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# =========================
# 工具函数
# =========================
def safe_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = re.sub(r'\s+', ' ', name)
    return name[:150] if name else "未命名"


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def read_urls(file_path: str):
    if not os.path.exists(file_path):
        logger.error(f"输入文件不存在: {file_path}")
        return []

    urls = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


def save_json(data, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path: str):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--lang=zh-CN")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def wait_for_nuxt(driver, timeout=20):
    logger.info("等待 window.__NUXT__ 加载完成...")
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return typeof window.__NUXT__ !== 'undefined' && window.__NUXT__ != null")
        )
        logger.info("window.__NUXT__ 已出现")
        return True
    except Exception as e:
        logger.error(f"等待 window.__NUXT__ 超时: {e}")
        return False


def get_page_title(driver):
    title = driver.title or "未命名作品"
    return safe_name(title.split("｜")[0].strip())


def get_chapters_from_work_page(driver):
    script = """
    const nuxt = window.__NUXT__;
    if (!nuxt || !nuxt.data || !nuxt.data[0] || !nuxt.data[0].comics) {
        return [];
    }
    return nuxt.data[0].comics.map(x => ({
        title: x.title,
        url: `https://www.kuaikanmanhua.com/web/comic/${x.id}`
    }));
    """
    for attempt in range(1, PAGE_READY_RETRY + 2):
        try:
            chapters = driver.execute_script(script)
            if chapters:
                return chapters
            logger.warning(f"章节数据为空，重试第 {attempt} 次")
        except Exception as e:
            logger.warning(f"提取章节列表失败，重试第 {attempt} 次: {e}")
        time.sleep(1)
    logger.error("最终未获取到章节列表")
    return []


def get_images_from_chapter_page(driver):
    script = """
    const nuxt = window.__NUXT__;
    if (!nuxt || !nuxt.data || !nuxt.data[0] || !nuxt.data[0].res ||
        !nuxt.data[0].res.data || !nuxt.data[0].res.data.comic_info ||
        !nuxt.data[0].res.data.comic_info.comic_images) {
        return [];
    }
    return nuxt.data[0].res.data.comic_info.comic_images.map(x => x.url1280 || x.url).filter(Boolean);
    """
    for attempt in range(1, PAGE_READY_RETRY + 2):
        try:
            images = driver.execute_script(script)
            if images:
                return images
            logger.warning(f"图片数据为空，重试第 {attempt} 次")
        except Exception as e:
            logger.warning(f"提取图片列表失败，重试第 {attempt} 次: {e}")
        time.sleep(1)
    logger.error("最终未获取到图片列表")
    return []


def chapter_done(chapter_dir: str) -> bool:
    done_flag = os.path.join(chapter_dir, ".done")
    if os.path.exists(done_flag):
        return True

    if os.path.exists(chapter_dir):
        for name in os.listdir(chapter_dir):
            if name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                return True
    return False


def mark_chapter_done(chapter_dir: str):
    done_flag = os.path.join(chapter_dir, ".done")
    with open(done_flag, "w", encoding="utf-8") as f:
        f.write("done")


def get_ext_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    if path.endswith(".png"):
        return ".png"
    if path.endswith(".webp"):
        return ".webp"
    if path.endswith(".jpeg"):
        return ".jpeg"
    return ".jpg"


def create_requests_session():
    session = requests.Session()
    retry = Retry(
        total=DOWNLOAD_RETRY_TIMES,
        read=DOWNLOAD_RETRY_TIMES,
        connect=DOWNLOAD_RETRY_TIMES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET", "HEAD"])
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def download_one_image(session, img_url, file_path, index, total):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.kuaikanmanhua.com/"
    }

    for attempt in range(1, DOWNLOAD_RETRY_TIMES + 2):
        try:
            logger.info(f"下载图片 [{index}/{total}] 第 {attempt} 次: {img_url}")
            resp = session.get(img_url, headers=headers, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()

            with open(file_path, "wb") as f:
                f.write(resp.content)

            if os.path.getsize(file_path) == 0:
                raise Exception("文件大小为0")

            return True
        except Exception as e:
            logger.warning(f"下载失败 [{index}/{total}] 第 {attempt} 次: {e}")
            if attempt < DOWNLOAD_RETRY_TIMES + 1:
                time.sleep(DOWNLOAD_RETRY_SLEEP)

    logger.error(f"图片最终下载失败: {img_url}")
    return False


def download_images(image_urls, chapter_dir):
    ensure_dir(chapter_dir)
    session = create_requests_session()

    total = len(image_urls)
    success_count = 0

    for idx, img_url in enumerate(image_urls, start=1):
        ext = get_ext_from_url(img_url)
        filename = f"{idx:03d}{ext}"
        file_path = os.path.join(chapter_dir, filename)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            logger.info(f"已存在，跳过: {file_path}")
            success_count += 1
            continue

        ok = download_one_image(session, img_url, file_path, idx, total)
        if ok:
            success_count += 1

    logger.info(f"章节图片下载完成: 成功 {success_count}/{total}")
    return success_count == total


def add_chapter_index(chapters):
    total = len(chapters)
    width = max(3, len(str(total)))

    new_list = []
    for idx, item in enumerate(chapters, start=1):
        title = safe_name(item.get("title", f"第{idx}话"))
        indexed_title = f"{idx:0{width}d}_{title}"
        new_item = {
            "index": idx,
            "title": title,
            "dir_name": indexed_title,
            "url": item["url"]
        }
        new_list.append(new_item)
    return new_list


def wait_for_manual_login_once():
    """
    本次程序运行期间仅等待一次手动登录
    """
    global LOGIN_CONFIRMED_THIS_RUN

    if LOGIN_CONFIRMED_THIS_RUN:
        logger.info("本次运行已完成登录确认，跳过")
        return

    print("\n" + "=" * 60)
    print("已成功打开作品页并获取章节信息。")
    print("请现在在浏览器中手动登录会员账号。")
    print("登录完成后，请在控制台输入 yes 并回车继续。")
    print("=" * 60 + "\n")

    while True:
        answer = input("请输入 yes 继续：").strip().lower()
        if answer == "yes":
            LOGIN_CONFIRMED_THIS_RUN = True
            logger.info("已收到 yes，本次运行后续不再要求登录")
            break
        else:
            print("输入无效，请输入 yes")


def process_work(driver, work_url: str):
    global LOGIN_CONFIRMED_THIS_RUN

    logger.info(f"开始处理作品页: {work_url}")
    driver.get(work_url)

    if not wait_for_nuxt(driver, NUXT_WAIT_TIMEOUT):
        logger.warning(f"作品页未加载出 window.__NUXT__，跳过: {work_url}")
        return

    work_title = get_page_title(driver)
    work_dir = os.path.join(OUTPUT_ROOT, work_title)
    ensure_dir(work_dir)

    logger.info(f"作品标题: {work_title}")
    logger.info(f"作品目录: {work_dir}")

    chapters_cache_path = os.path.join(work_dir, CHAPTER_CACHE_FILENAME)

    chapters = load_json(chapters_cache_path)
    if chapters:
        logger.info(f"检测到章节缓存，直接使用: {chapters_cache_path}")
    else:
        raw_chapters = get_chapters_from_work_page(driver)
        if not raw_chapters:
            logger.warning(f"未获取到章节信息，跳过作品: {work_url}")
            return

        chapters = add_chapter_index(raw_chapters)
        save_json(chapters, chapters_cache_path)
        logger.info(f"章节缓存已保存: {chapters_cache_path}")

    # 程序启动后仅要求登录一次：
    # 在第一次成功打开作品页且拿到章节信息后触发
    if not LOGIN_CONFIRMED_THIS_RUN:
        wait_for_manual_login_once()

    for i, chapter in enumerate(chapters, start=1):
        chapter_title = chapter["title"]
        chapter_dir_name = safe_name(chapter.get("dir_name") or chapter_title)
        chapter_url = chapter["url"]
        chapter_dir = os.path.join(work_dir, chapter_dir_name)

        logger.info(f"处理章节 [{i}/{len(chapters)}]: {chapter_dir_name}")
        logger.info(f"章节URL: {chapter_url}")

        if SKIP_IF_CHAPTER_DONE and chapter_done(chapter_dir):
            logger.info(f"章节已爬取，跳过: {chapter_dir_name}")
            continue

        ensure_dir(chapter_dir)

        try:
            driver.get(chapter_url)

            if not wait_for_nuxt(driver, NUXT_WAIT_TIMEOUT):
                logger.warning(f"章节页未加载出 window.__NUXT__，跳过: {chapter_dir_name}")
                continue

            image_urls = get_images_from_chapter_page(driver)
            if not image_urls:
                logger.warning(f"章节无图片，跳过: {chapter_dir_name}")
                continue

            ok = download_images(image_urls, chapter_dir)
            if ok:
                mark_chapter_done(chapter_dir)
                logger.info(f"章节完成: {chapter_dir_name}")
            else:
                logger.warning(f"章节未完全下载成功: {chapter_dir_name}")

        except Exception as e:
            logger.error(f"处理章节失败: {chapter_dir_name}, 错误: {e}")

        logger.info(f"暂停 {PAUSE_SECONDS} 秒")
        time.sleep(PAUSE_SECONDS)


def main():
    ensure_dir(OUTPUT_ROOT)
    urls = read_urls(INPUT_FILE)
    if not urls:
        logger.error("没有读取到任何作品页 URL")
        return

    driver = None
    try:
        driver = create_driver()
        for work_url in urls:
            try:
                process_work(driver, work_url)
            except Exception as e:
                logger.error(f"处理作品失败: {work_url}, 错误: {e}")
    finally:
        if driver:
            driver.quit()
        logger.info("任务结束")


if __name__ == "__main__":
    main()
