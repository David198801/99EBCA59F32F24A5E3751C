import os.path

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


# 是否跳过已存在？
is_pass_exists = True

# 代理
# proxies = None
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890',
}

SCENARIO_URL = "https://bestdori.com/tool/explorer/asset/jp/sound/voice/scenario"
FILE_SCENARIO_URL = "https://bestdori.com/assets/jp/sound/voice/scenario"

# 指定chromedriver的路径
driver_path = r'E:\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# 创建 ChromeOptions 实例 (可选)
chrome_options = Options()

# 创建浏览器驱动实例
driver = webdriver.Chrome(service=service)

# 文件输出路径
mp3_out_path = r"E:/bestdori/mp3"
mp3_txt_path = mp3_out_path + "/mp3links.txt"


# 获取包含mp3的包的路径, [{'relative_path': 'actionset/group0', 'url': 'https://bestdori.com/tool/explorer/asset/jp/scenario/actionset/group0'}]
def get_assets_zip_url(url, mp3_zip_urls):
    # 打开指定的URL
    driver.get(url)
    time.sleep(3)
    page_source = driver.page_source

    # 使用BeautifulSoup解析
    soup = BeautifulSoup(page_source, 'html.parser')

    # 查找所有包含fas fa-file-archive图标的<span>标签的下一个兄弟标签
    spans = soup.find_all('span', class_='icon')
    for span in spans:
        if span.find('i', class_='fas fa-file-archive'):
            file_name = span.find_next_sibling('span', class_='m-l-xs').text.strip()
            full_url = url + "/" + file_name
            mp3_zip_urls.append({
                "relative_path": full_url.replace(SCENARIO_URL + "/", ""),
                "url": full_url
            })
        elif span.find('i', class_='fas fa-folder'):
            dir_name = span.find_next_sibling('span', class_='m-l-xs').text.strip()
            full_url = url + "/" + dir_name
            get_assets_zip_url(full_url, mp3_zip_urls)


def check_and_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 获取assets文件的路径{相对路径,[url1,url2]}
def get_assets_url(mp3_zip_urls, mp3_urls):
    check_and_make_dir(mp3_out_path)

    all_content = ""
    if os.path.exists(mp3_txt_path):
        with open(mp3_txt_path, "r", encoding="utf-8") as txt:
            all_content = txt.read()

    txt = open(mp3_txt_path, "a", encoding="utf-8")
    for d in mp3_zip_urls:
        relative_path = d['relative_path']
        assets_url = d['url']

        dir_path = FILE_SCENARIO_URL + "/" + relative_path + "_rip/"
        if dir_path in all_content:
            print("跳过 "+dir_path)
            continue

        print("正在处理 " + relative_path)
        # 打开指定的URL
        driver.get(assets_url)
        time.sleep(1)
        page_source = driver.page_source
        # 使用BeautifulSoup解析
        soup = BeautifulSoup(page_source, 'html.parser')

        # 查找所有具有fas fa-file-audio图标的<span>标签的下一个兄弟标签
        spans = soup.find_all('span', class_='icon')
        file_names = [span.find_next_sibling().text.strip() for span in spans if span.find('i', class_='fas fa-file-audio')]
        for file_name in file_names:
            full_link = dir_path + file_name
            txt.write(full_link + "\n")
        txt.flush()
    txt.close()




if __name__ == '__main__':

    mp3_urls = {}

    mp3_zip_urls = []
    # 解析包含下载链接的包
    get_assets_zip_url(SCENARIO_URL, mp3_zip_urls)

    # 测试用，只取第一条
    # mp3_zip_urls = mp3_zip_urls[:1]
    # 解析下载链接
    get_assets_url(mp3_zip_urls, mp3_urls)



# 关闭浏览器
driver.quit()
