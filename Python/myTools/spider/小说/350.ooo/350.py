from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time


def read_urls(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def create_driver():
    service = Service(r"d:\cmd\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(15)
    return driver


def scrape_chapter(driver, url):
    wait = WebDriverWait(driver, 5)

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

    # 获取标题
    try:
        elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        text = elem.text.strip()
        if text:
            title = text
    except Exception:
        print("标题获取失败")

    # 获取正文
    try:
        content_div = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article#article"))
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
        f.write(f"第{index}章\n")
        f.write(f"标题：{title}\n")
        # f.write(f"链接：{url}\n\n")

        if paragraphs:
            for p in paragraphs:
                f.write(p + "\n")
        else:
            f.write("【正文未获取到】\n")

        f.write("\n" + "=" * 50 + "\n\n")


def main():
    input_file = "chapters.txt"
    output_file = "output.txt"

    open(output_file, "w", encoding="utf-8").close()

    urls = read_urls(input_file)
    driver = create_driver()

    try:
        for i, url in enumerate(urls, 1):
            print(f"正在处理第 {i} 个: {url}")
            try:
                title, paragraphs = scrape_chapter(driver, url)
                append_to_txt(output_file, i, url, title, paragraphs)
                print(f"第 {i} 章已写入")
                time.sleep(1)
            except Exception as e:
                print(f"抓取失败: {url}")
                print(e)
                append_to_txt(output_file, i, url, "抓取失败", ["本章内容未成功获取"])
    finally:
        driver.quit()

    print("全部完成")


if __name__ == "__main__":
    main()