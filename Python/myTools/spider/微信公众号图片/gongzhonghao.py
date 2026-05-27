import os
import re
import time
import random
import logging
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ========== 配置 ==========
TXT_FILE = "公众号文章.txt"
SAVE_ROOT = "下载图片"
CHROMEDRIVER_PATH = r"D:\cmd\chromedriver.exe"  # 如果已加入PATH可直接写 chromedriver；否则写完整路径
HEADLESS = False  # True 表示无界面模式
PAGE_LOAD_TIMEOUT = 30
WAIT_TIMEOUT = 20

DOWNLOAD_RETRY = 3          # 下载失败重试次数
DOWNLOAD_RETRY_SLEEP = 2    # 每次重试前等待秒数

ARTICLE_WAIT_SECONDS = 3    # 每篇文章处理完成后固定等待秒数
USE_RANDOM_WAIT = True      # 是否启用随机等待，启用后优先使用随机秒数
ARTICLE_WAIT_MIN = 1        # 随机等待最小秒数
ARTICLE_WAIT_MAX = 3        # 随机等待最大秒数

LOG_FILE = "crawler.log"                # 日志文件
PROCESSED_URLS_FILE = "processed_urls.txt"  # 已处理 URL 记录文件
# ==========================


def setup_logger():
    """配置日志：同时输出到控制台和文件"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 避免重复添加 handler
    if logger.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 文件日志
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_processed_urls():
    """读取已处理 URL 集合"""
    if not os.path.exists(PROCESSED_URLS_FILE):
        return set()

    with open(PROCESSED_URLS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def save_processed_url(url):
    """追加保存已处理 URL"""
    with open(PROCESSED_URLS_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")


def sanitize_filename(name):
    """清理文件/文件夹名中的非法字符"""
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name if name else "未命名标题"


def get_file_ext_from_url(url):
    """尽量从 URL 中提取扩展名，没有则默认 jpg"""
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"]:
        return ext
    return ".jpg"


def make_unique_dir(base_dir):
    """如果目录已存在，则自动添加后缀避免冲突"""
    if not os.path.exists(base_dir):
        return base_dir

    index = 1
    while True:
        new_dir = f"{base_dir}_{index}"
        if not os.path.exists(new_dir):
            return new_dir
        index += 1


def convert_to_hd_image_url(img_url):
    """
    将图片地址最后一段的尺寸标记改为 /0
    例如：
    .../640   -> .../0
    .../320   -> .../0
    .../1080  -> .../0
    """
    parsed = urlparse(img_url)
    path = parsed.path
    new_path = re.sub(r'/\d+$', '/0', path)

    if new_path != path:
        return parsed._replace(path=new_path).geturl()
    return img_url


def download_image(img_url, save_path, referer="https://mp.weixin.qq.com/"):
    """下载单张图片，支持失败重试"""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": referer
    }

    candidate_urls = []
    hd_url = convert_to_hd_image_url(img_url)
    candidate_urls.append(hd_url)
    if hd_url != img_url:
        candidate_urls.append(img_url)

    for candidate_url in candidate_urls:
        for attempt in range(1, DOWNLOAD_RETRY + 1):
            try:
                logging.info(f"尝试下载({attempt}/{DOWNLOAD_RETRY}): {candidate_url}")
                resp = requests.get(candidate_url, headers=headers, timeout=30)
                resp.raise_for_status()

                with open(save_path, "wb") as f:
                    f.write(resp.content)

                logging.info(f"下载成功: {save_path}")
                return True
            except Exception as e:
                logging.warning(f"下载失败({attempt}/{DOWNLOAD_RETRY}): {candidate_url} -> {e}")
                if attempt < DOWNLOAD_RETRY:
                    time.sleep(DOWNLOAD_RETRY_SLEEP)

        logging.warning(f"地址下载全部重试失败，尝试下一个地址: {candidate_url}")

    logging.error(f"最终下载失败: {img_url}")
    return False


def get_title_from_page_content(driver):
    """
    从 id=page-content 的 div 下，
    获取内部间接的 class=rich_media_title 的 h1，
    并把内部多个 span 文本用空格拼接
    """
    page_content = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "page-content"))
    )

    h1 = page_content.find_element(By.CSS_SELECTOR, "h1.rich_media_title")

    spans = h1.find_elements(By.TAG_NAME, "span")
    if spans:
        texts = [span.text.strip() for span in spans if span.text.strip()]
        title = " ".join(texts).strip()
        if title:
            return title

    title = h1.text.strip()
    return title if title else "未命名标题"


def get_image_urls_from_cgi_data(driver):
    """
    直接从 window.cgiDataNew.picture_page_info_list 获取图片列表，
    每个元素的 cdn_url 属性就是图片地址
    """
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        lambda d: d.execute_script(
            "return !!(window.cgiDataNew && Array.isArray(window.cgiDataNew.picture_page_info_list));"
        )
    )

    picture_list = driver.execute_script("""
        return (window.cgiDataNew && window.cgiDataNew.picture_page_info_list) || [];
    """)

    img_urls = []
    for item in picture_list:
        if isinstance(item, dict):
            cdn_url = item.get("cdn_url")
            if cdn_url and isinstance(cdn_url, str):
                img_urls.append(cdn_url)

    # 去重，保留顺序
    unique_urls = []
    seen = set()
    for url in img_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls


def init_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("--blink-settings=imagesEnabled=true")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver


def wait_after_article():
    """每篇文章处理完成后等待"""
    if USE_RANDOM_WAIT:
        seconds = random.uniform(ARTICLE_WAIT_MIN, ARTICLE_WAIT_MAX)
        logging.info(f"本篇文章处理完成，随机等待 {seconds:.2f} 秒后继续...")
        time.sleep(seconds)
    else:
        logging.info(f"本篇文章处理完成，等待 {ARTICLE_WAIT_SECONDS} 秒后继续...")
        time.sleep(ARTICLE_WAIT_SECONDS)


def process_url(driver, url):
    logging.info(f"正在处理: {url}")

    try:
        driver.get(url)
        time.sleep(3)
    except Exception as e:
        logging.error(f"页面打开失败: {url} -> {e}")
        return False

    try:
        title = get_title_from_page_content(driver)
        title = sanitize_filename(title)
        folder = make_unique_dir(os.path.join(SAVE_ROOT, title))
        os.makedirs(folder, exist_ok=True)
        logging.info(f"标题: {title}")
        logging.info(f"保存目录: {folder}")
    except Exception as e:
        logging.error(f"获取标题失败: {url} -> {e}")
        return False

    try:
        img_urls = get_image_urls_from_cgi_data(driver)
        logging.info(f"找到图片数量: {len(img_urls)}")
    except Exception as e:
        logging.error(f"获取图片列表失败: {url} -> {e}")
        return False

    if not img_urls:
        logging.warning("未找到符合条件的图片")
        return True  # 文章处理完了，只是没有图片

    for i, img_url in enumerate(img_urls, start=1):
        hd_url = convert_to_hd_image_url(img_url)
        ext = get_file_ext_from_url(hd_url)
        filename = f"{i:03d}{ext}"
        save_path = os.path.join(folder, filename)

        success = download_image(img_url, save_path, referer=url)
        if not success:
            logging.warning(f"图片下载失败，跳过: {img_url}")

    return True


def main():
    setup_logger()

    if not os.path.exists(TXT_FILE):
        logging.error(f"未找到文件: {TXT_FILE}")
        return

    os.makedirs(SAVE_ROOT, exist_ok=True)

    with open(TXT_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        logging.warning("未读取到任何 URL")
        return

    processed_urls = load_processed_urls()
    logging.info(f"已处理 URL 数量: {len(processed_urls)}")

    driver = init_driver()

    try:
        total = len(urls)
        for idx, url in enumerate(urls, start=1):
            if url in processed_urls:
                logging.info(f"跳过已处理 URL ({idx}/{total}): {url}")
                continue

            logging.info(f"===== 进度: {idx}/{total} =====")
            success = process_url(driver, url)

            if success:
                save_processed_url(url)
                processed_urls.add(url)
                logging.info(f"已记录处理完成 URL: {url}")
            else:
                logging.warning(f"本次处理失败，不记录 URL，后续可重试: {url}")

            wait_after_article()
    finally:
        driver.quit()
        logging.info("浏览器已关闭，程序结束")


if __name__ == "__main__":
    main()