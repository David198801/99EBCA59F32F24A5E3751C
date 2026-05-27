import os
import re
import time
import json
import random
import logging
from pathlib import Path
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException


# =========================
# 基础配置
# =========================
TXT_FILE = "爱奇艺叭嗒.txt"
BASE_SAVE_DIR = "downloads"
CHROMEDRIVER_PATH = "chromedriver.exe"   # 如果已加入环境变量，可改为 None
HEADLESS = False                         # True 为无头模式
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 8

REQUEST_TIMEOUT = 20
CHAPTER_SLEEP_SECONDS = 3                # 每章下载完成后暂停秒数
IMAGE_RETRY = 3                          # 单张图片下载重试次数
CHAPTER_RETRY = 2                        # 单章节抓取重试次数

# 日志文件
LOG_FILE = "spider.log"


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
def sanitize_filename(name: str) -> str:
    """清理非法文件名字符"""
    name = re.sub(r'[\\/:*?"<>|]+', '_', name)
    name = name.strip().strip(".")
    return name or "未命名"


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def read_urls(txt_file):
    """从 txt 文件读取作品 url"""
    if not os.path.exists(txt_file):
        raise FileNotFoundError(f"未找到文件: {txt_file}")

    urls = []
    with open(txt_file, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if url and url.startswith("http"):
                urls.append(url)
    return urls


def build_requests_session():
    """构建带重试的 requests session"""
    session = requests.Session()

    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    })
    return session


def create_driver():
    """创建 ChromeDriver"""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=zh-CN")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if CHROMEDRIVER_PATH and os.path.exists(CHROMEDRIVER_PATH):
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(IMPLICIT_WAIT)

    # 尝试去除 webdriver 特征
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """
            }
        )
    except Exception:
        pass

    return driver


def get_comic_info(driver, work_url):
    """
    打开作品页，获取第一个拥有 data-comicid、data-comictitle 的标签
    返回: comic_id, comic_title
    """
    logger.info(f"打开作品页: {work_url}")
    driver.get(work_url)
    time.sleep(2)

    script = """
    const elem = document.querySelector('[data-comicid][data-comictitle]');
    if (!elem) return null;
    return {
        comicId: elem.getAttribute('data-comicid'),
        comicTitle: elem.getAttribute('data-comictitle')
    };
    """
    result = driver.execute_script(script)

    if not result:
        raise ValueError(f"未找到 data-comicid 和 data-comictitle: {work_url}")

    comic_id = str(result.get("comicId", "")).strip()
    comic_title = str(result.get("comicTitle", "")).strip()

    if not comic_id or not comic_title:
        raise ValueError(f"漫画信息提取失败: {work_url}")

    logger.info(f"获取漫画信息成功: comic_id={comic_id}, comic_title={comic_title}")
    return comic_id, sanitize_filename(comic_title)


def get_catalog_json(session, comic_id, referer_url=None):
    """
    请求目录接口
    https://www.iqiyi.com/manhua/catalog/{漫画id}/
    """
    url = f"https://www.iqiyi.com/manhua/catalog/{comic_id}/"
    headers = {}
    if referer_url:
        headers["Referer"] = referer_url

    logger.info(f"请求目录接口: {url}")
    resp = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    # 尝试解析 JSON
    try:
        data = resp.json()
    except Exception:
        # 某些情况可能返回文本
        text = resp.text.strip()
        data = json.loads(text)

    return data


def parse_episodes(catalog_json):
    """从目录 json 的 data.episodes 中获取 episodes 数组"""
    data = catalog_json.get("data", {})
    if not isinstance(data, dict):
        raise ValueError("目录接口中 data 不是对象")

    episodes = data.get("episodes", [])
    if not isinstance(episodes, list):
        raise ValueError("目录接口中 data.episodes 不是数组")

    return episodes


def get_chapter_image_urls(driver, comic_id, episode_id):
    """
    进入章节页，获取 <ul class="main-container"> 内所有 img 的图片地址
    优先 data-original，否则 src
    """
    chapter_url = f"https://www.iqiyi.com/manhua/reader/{comic_id}_{episode_id}.html"
    logger.info(f"进入章节页: {chapter_url}")
    driver.get(chapter_url)

    # 等待页面图片加载
    time.sleep(3)

    script = """
    const ul = document.querySelector('ul.main-container');
    if (!ul) return [];
    const imgs = ul.querySelectorAll('img');
    const urls = [];
    imgs.forEach(img => {
        let u = img.getAttribute('data-original') || img.getAttribute('src');
        if (u) urls.push(u);
    });
    return urls;
    """
    urls = driver.execute_script(script)

    # 去重并过滤
    new_urls = []
    seen = set()
    for u in urls:
        if not u:
            continue
        u = u.strip()
        if u.startswith("//"):
            u = "https:" + u
        if u not in seen:
            seen.add(u)
            new_urls.append(u)

    if not new_urls:
        logger.warning(f"章节没有获取到图片: {chapter_url}")

    return new_urls, chapter_url


def get_image_ext(image_url, response=None):
    """尽量推断图片扩展名"""
    path = image_url.split("?")[0].lower()
    for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext

    if response is not None:
        content_type = response.headers.get("Content-Type", "").lower()
        if "png" in content_type:
            return ".png"
        elif "webp" in content_type:
            return ".webp"
        elif "gif" in content_type:
            return ".gif"

    return ".jpg"


def download_image(session, image_url, save_path, referer=None, retries=IMAGE_RETRY):
    """下载单张图片，支持重试"""
    headers = {}
    if referer:
        headers["Referer"] = referer

    last_error = None
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(image_url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
            resp.raise_for_status()

            tmp_path = str(save_path) + ".tmp"
            with open(tmp_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            os.replace(tmp_path, save_path)
            return True
        except Exception as e:
            last_error = e
            logger.warning(f"下载失败，第 {attempt}/{retries} 次: {image_url} -> {e}")
            time.sleep(1.5 * attempt)

    logger.error(f"图片下载最终失败: {image_url}, 错误: {last_error}")
    return False


def download_chapter(driver, session, comic_id, comic_title, episode, comic_dir):
    """下载单个章节"""
    episode_title = str(episode.get("episodeTitle", "")).strip()
    episode_id = str(episode.get("episodeId", "")).strip()

    if not episode_title or not episode_id:
        logger.warning(f"跳过异常章节数据: {episode}")
        return False

    safe_episode_title = sanitize_filename(episode_title)
    chapter_dir = os.path.join(comic_dir, safe_episode_title)
    ensure_dir(chapter_dir)

    # 若已有图片，默认认为章节已下载过
    existing_files = [f for f in os.listdir(chapter_dir) if re.match(r"^\d{3}\.", f)]
    if existing_files:
        logger.info(f"章节已存在，跳过: {comic_title} - {safe_episode_title}")
        return True

    for attempt in range(1, CHAPTER_RETRY + 1):
        try:
            image_urls, chapter_url = get_chapter_image_urls(driver, comic_id, episode_id)

            if not image_urls:
                raise ValueError("未获取到章节图片 URL")

            success_count = 0
            total = len(image_urls)

            for idx, image_url in enumerate(image_urls, start=1):
                file_num = f"{idx:03d}"

                # 先尝试探测扩展名
                ext = get_image_ext(image_url)
                save_path = os.path.join(chapter_dir, file_num + ext)

                if os.path.exists(save_path):
                    logger.info(f"图片已存在，跳过: {save_path}")
                    success_count += 1
                    continue

                ok = download_image(
                    session=session,
                    image_url=image_url,
                    save_path=save_path,
                    referer=chapter_url,
                    retries=IMAGE_RETRY
                )

                if ok:
                    logger.info(f"下载成功 [{idx}/{total}] {save_path}")
                    success_count += 1
                else:
                    logger.error(f"下载失败 [{idx}/{total}] {image_url}")

            if success_count == total:
                logger.info(f"章节下载完成: {comic_title} - {safe_episode_title}")
                return True
            else:
                raise RuntimeError(f"章节下载不完整: 成功 {success_count}/{total}")

        except Exception as e:
            logger.warning(f"章节抓取失败，第 {attempt}/{CHAPTER_RETRY} 次: {safe_episode_title}, 错误: {e}")
            time.sleep(2 * attempt)

    logger.error(f"章节最终失败: {comic_title} - {safe_episode_title}")
    return False


def main():
    ensure_dir(BASE_SAVE_DIR)

    try:
        urls = read_urls(TXT_FILE)
    except Exception as e:
        logger.error(f"读取 URL 文件失败: {e}")
        return

    if not urls:
        logger.warning("未读取到任何作品 URL")
        return

    session = build_requests_session()
    driver = create_driver()

    try:
        for work_url in urls:
            try:
                comic_id, comic_title = get_comic_info(driver, work_url)
                comic_dir = os.path.join(BASE_SAVE_DIR, comic_title)
                ensure_dir(comic_dir)

                catalog_json = get_catalog_json(session, comic_id, referer_url=work_url)
                episodes = parse_episodes(catalog_json)

                if not episodes:
                    logger.warning(f"该漫画没有章节: {comic_title}")
                    continue

                logger.info(f"开始下载漫画: {comic_title}，章节数: {len(episodes)}")

                for i, episode in enumerate(episodes, start=1):
                    episode_title = sanitize_filename(str(episode.get("episodeTitle", "")).strip())
                    logger.info(f"开始章节 [{i}/{len(episodes)}]: {episode_title}")

                    ok = download_chapter(
                        driver=driver,
                        session=session,
                        comic_id=comic_id,
                        comic_title=comic_title,
                        episode=episode,
                        comic_dir=comic_dir
                    )

                    if ok:
                        logger.info(f"章节完成，暂停 {CHAPTER_SLEEP_SECONDS} 秒")
                    else:
                        logger.error(f"章节失败: {comic_title} - {episode_title}，暂停 {CHAPTER_SLEEP_SECONDS} 秒")

                    time.sleep(CHAPTER_SLEEP_SECONDS + random.uniform(0.5, 1.5))

            except Exception as e:
                logger.error(f"作品处理失败: {work_url}, 错误: {e}")

    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
