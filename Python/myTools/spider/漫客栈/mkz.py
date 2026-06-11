import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

# =========================
# 硬编码配置
# =========================

COMIC_URL = "https://www.mkzhan.com/210485/"  # 替换成实际漫画链接

# 图片接口模板，后续只替换 comic_id 和 chapter_id
API_TEMPLATE = (
    "https://comic.mkzcdn.com/chapter/content/v1/?chapter_id=566678&comic_id=210485&format=1&quality=1&sign=7e5d6f89e04a21fc87682e8dff7f6a39&type=1&uid=83172733"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": COMIC_URL,
}


# =========================
# 工具函数
# =========================

def safe_filename(name: str) -> str:
    """清理非法文件名字符"""
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    return name


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def get_extension_from_url(url: str) -> str:
    """从图片URL猜测扩展名"""
    parsed = urlparse(url)
    path = parsed.path.lower()

    for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        if path.endswith(ext):
            return ext

    return ".jpg"


def build_api_url(template: str, comic_id: str, chapter_id: str) -> str:
    """替换模板中的 comic_id 和 chapter_id"""
    new_url = re.sub(r"chapter_id=\d+", f"chapter_id={chapter_id}", template)
    new_url = re.sub(r"comic_id=\d+", f"comic_id={comic_id}", new_url)
    return new_url


def extract_ids_from_href(href: str):
    """
    从章节 href 中提取 comic_id 和 chapter_id
    例如: /210485/566699.html
    """
    m = re.search(r"/(\d+)/(\d+)\.html", href)
    if not m:
        return None, None
    return m.group(1), m.group(2)


# =========================
# 抓取漫画首页
# =========================

def fetch_comic_info(comic_url: str):
    """获取漫画标题和章节列表"""
    resp = requests.get(comic_url, headers=HEADERS, timeout=20, verify=False)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # 获取漫画标题
    title_tag = soup.select_one("p.comic-title.j-comic-title")
    if not title_tag:
        raise ValueError("未找到漫画标题：<p class='comic-title j-comic-title'>")
    comic_title = title_tag.get_text(strip=True)

    # 获取章节列表容器
    chapter_container = soup.select_one("div.chapter__list.clearfix")
    if not chapter_container:
        raise ValueError("未找到章节列表：<div class='chapter__list clearfix'>")

    chapters = []
    for a in chapter_container.select("a.j-chapter-link"):
        href = a.get("data-hreflink", "").strip()
        if not href:
            continue

        chapter_title = a.get_text(strip=True)
        comic_id, chapter_id = extract_ids_from_href(href)

        if not comic_id or not chapter_id:
            continue

        chapters.append({
            "chapter_title": chapter_title,
            "href": href,
            "comic_id": comic_id,
            "chapter_id": chapter_id
        })

    if not chapters:
        raise ValueError("未解析到任何章节")

    return comic_title, chapters


# =========================
# 获取章节图片列表
# =========================

def fetch_chapter_images(comic_id: str, chapter_id: str):
    api_url = build_api_url(API_TEMPLATE, comic_id, chapter_id)

    resp = requests.get(api_url, headers=HEADERS, timeout=20, verify=False)
    resp.raise_for_status()

    data = resp.json()

    pages = data.get("data", {}).get("page", [])
    image_urls = []

    for page in pages:
        image_url = page.get("image")
        if image_url:
            image_urls.append(image_url)

    return image_urls


# =========================
# 下载图片
# =========================

def download_image(url: str, save_path: str):
    with requests.get(url, headers=HEADERS, timeout=30, stream=True, verify=False) as resp:
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def download_chapter(comic_title: str, chapter_title: str, image_urls: list):
    comic_title_safe = safe_filename(comic_title)
    chapter_title_safe = safe_filename(chapter_title)

    output_dir = os.path.join("output", comic_title_safe, chapter_title_safe)
    ensure_dir(output_dir)

    total = len(image_urls)
    for idx, img_url in enumerate(image_urls, start=1):
        ext = get_extension_from_url(img_url)
        filename = f"{idx:03d}{ext}"
        save_path = os.path.join(output_dir, filename)

        if os.path.exists(save_path):
            print(f"[跳过] 已存在: {save_path}")
            continue

        try:
            print(f"[下载] ({idx}/{total}) {img_url}")
            download_image(img_url, save_path)
        except Exception as e:
            print(f"[失败] {img_url} -> {e}")


# =========================
# 主流程
# =========================

def main():
    print("[1] 获取漫画信息...")
    comic_title, chapters = fetch_comic_info(COMIC_URL)
    print(f"漫画标题: {comic_title}")
    print(f"章节数量: {len(chapters)}")

    for i, chapter in enumerate(chapters, start=1):
        chapter_title = chapter["chapter_title"]
        comic_id = chapter["comic_id"]
        chapter_id = chapter["chapter_id"]

        print(f"\n[2] 处理章节 ({i}/{len(chapters)}): {chapter_title}")
        print(f"comic_id={comic_id}, chapter_id={chapter_id}")

        try:
            image_urls = fetch_chapter_images(comic_id, chapter_id)
            print(f"图片数量: {len(image_urls)}")

            if not image_urls:
                print("[跳过] 没有获取到图片")
                continue

            download_chapter(comic_title, chapter_title, image_urls)
        except Exception as e:
            print(f"[失败] 章节处理失败: {chapter_title} -> {e}")


if __name__ == "__main__":
    # 关闭 https://127.0.0.1 自签名证书警告
    requests.packages.urllib3.disable_warnings()
    main()