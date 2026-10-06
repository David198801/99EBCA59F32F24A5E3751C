from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
import re


# ====== 硬编码配置（放在脚本头部） ======
URL_TEMPLATE = "https://www.quanben5.com/n/xiuxiansuchengzhinan/{num}.html"
START_CHAPTER = 16602
END_CHAPTER = 16678
OUTPUT_FILE = "output.txt"
CHROMEDRIVER_PATH = r"d:\cmd\chromedriver.exe"
# ====================================
def generate_urls(url_template, start_chapter, end_chapter):
    """
    根据模板 URL、起始编号和结束编号生成章节链接
    模板中必须包含 {num} 占位符
    例如：
        https://www.quanben5.com/n/xiuxiansuchengzhinan/{num}.html
    """
    if "{num}" not in url_template:
        raise ValueError("URL_TEMPLATE 必须包含 {num} 占位符")
    if start_chapter > end_chapter:
        raise ValueError("START_CHAPTER 不能大于 END_CHAPTER")
    urls = [url_template.format(num=i) for i in range(start_chapter, end_chapter + 1)]
    return urls


def create_driver():
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(15)
    return driver


def scrape_chapter(driver, url):
    wait = WebDriverWait(driver, 10)

    try:
        print("开始打开页面:", url)
        driver.get(url)
        print("页面打开完成")
    except TimeoutException:
        print("页面加载超时，停止加载并尝试抓取已加载内容")
        try:
            driver.execute_script("window.stop();")
        except:
            pass

    title = "未获取到标题"
    paragraphs = []

    try:
        elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title1"))
        )
        text = elem.text.strip()
        if text:
            title = text
    except Exception:
        print("标题获取失败")

    try:
        content_div = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#content"))
        )

        p_tags = content_div.find_elements(By.TAG_NAME, "p")
        paragraphs = [p.text.strip() for p in p_tags if p.text.strip()]

        if not paragraphs:
            raw_text = content_div.text.strip()
            if raw_text:
                paragraphs = [raw_text]
    except Exception:
        print("正文获取失败")

    return title, paragraphs


def append_to_txt(output_file, index, url, title, paragraphs):
    with open(output_file, "a", encoding="utf-8") as f:
        #f.write(f"第{index}章\n")
        f.write(f"{title}\n")
        # f.write(f"链接：{url}\n\n")

        if paragraphs:
            for p in paragraphs:
                f.write(p + "\n")
        else:
            f.write("【正文未获取到】\n")

        f.write("\n" + "=" * 50 + "\n\n")


def main():
    open(OUTPUT_FILE, "w", encoding="utf-8").close()

    urls = generate_urls(URL_TEMPLATE, START_CHAPTER, END_CHAPTER)
    driver = create_driver()

    try:
        for i, url in enumerate(urls, 1):
            print(f"正在处理第 {i} 章: {url}")
            try:
                title, paragraphs = scrape_chapter(driver, url)
                append_to_txt(OUTPUT_FILE, i, url, title, paragraphs)
                print(f"第 {i} 章已写入")
                time.sleep(1)
            except Exception as e:
                print(f"抓取失败: {url}")
                print(e)
                append_to_txt(OUTPUT_FILE, i, url, "抓取失败", ["本章内容未成功获取"])
    finally:
        driver.quit()

    print("全部完成")


if __name__ == "__main__":
    main()