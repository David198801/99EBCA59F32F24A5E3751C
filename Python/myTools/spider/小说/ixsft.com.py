# -*- coding: utf-8 -*-
import time
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


# ====== 硬编码配置（统一放这里） ======
START_URL = "https://www.ixsft.com/info/565530/139945902.html"
CHROMEDRIVER_PATH = r"d:\cmd\chromedriver.exe"
OUTPUT_TXT = "绝对命运游戏.txt"
PAGE_LOAD_TIMEOUT = 15
SLEEP_SECONDS = 2
CHAPTER_SEPARATOR = "\n\n" + "=" * 50 + "\n\n"


def create_driver():
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver


def init_output_file(txt_path):
    """每次运行先覆盖输出文件。"""
    with open(txt_path, "w", encoding="utf-8"):
        pass


def get_article_text(driver):
    article = driver.find_element(By.ID, "article")
    return article.text.strip()


def get_next_info(driver):
    next_a = driver.find_element(By.ID, "pt_next")
    next_text = next_a.text.strip()
    next_href = next_a.get_attribute("href")
    return next_text, next_href


def save_page_text(f, content, is_next_chapter=False):
    f.write(content)

    if is_next_chapter:
        f.write(CHAPTER_SEPARATOR)
        f.flush()


def main():
    init_output_file(OUTPUT_TXT)

    driver = create_driver()
    visited = set()

    try:
        current_url = START_URL

        with open(OUTPUT_TXT, "a", encoding="utf-8") as f:
            while True:
                if current_url in visited:
                    print("检测到重复页面，停止，避免死循环：", current_url)
                    break
                visited.add(current_url)

                print("打开页面：", current_url)
                driver.get(current_url)
                time.sleep(SLEEP_SECONDS)

                # 获取正文
                try:
                    content = get_article_text(driver)
                except Exception as e:
                    print("获取正文失败：", e)
                    break

                # 获取下一步链接
                try:
                    next_text, next_href = get_next_info(driver)
                    print("pt_next 内容：", next_text, "链接：", next_href)
                except Exception as e:
                    print("获取 pt_next 失败：", e)
                    break

                # 写入 txt
                is_next_chapter = (next_text == "下一章")
                save_page_text(f, content, is_next_chapter=is_next_chapter)
                print("已写入：", current_url)

                # 判断下一步
                if next_text == "没有了":
                    print("已到结尾，程序结束。")
                    break
                elif next_text in ("下一页", "下一章"):
                    if not next_href:
                        print("未找到下一页链接，程序结束。")
                        break
                    current_url = urljoin(current_url, next_href)
                else:
                    print(f"遇到未知的 pt_next 文本: {next_text}，程序结束。")
                    break

    finally:
        driver.quit()


if __name__ == "__main__":
    main()