import os.path

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By

# 代理
# proxies = None
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890',
}

BGM_URL_S = ["https://bestdori.com/tool/explorer/asset/jp/sound/scenario/bgm"]

TIME_DELAY = 3

# 指定chromedriver的路径
driver_path = r'E:\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# 创建 ChromeOptions 实例 (可选)
chrome_options = Options()

# 创建浏览器驱动实例
driver = webdriver.Chrome(service=service)

# 文件输出路径
out_path = r"E:\素材用\bangdream bgm"


def get_mp3_urls(mp3_urls):
    for explorer_url in BGM_URL_S:
        # 打开指定的URL
        driver.get(explorer_url)
        time.sleep(TIME_DELAY)
        page_source = driver.page_source

        # 使用BeautifulSoup解析
        soup = BeautifulSoup(page_source, 'html.parser')

        # 查找所有包含fas fa-file-archive图标的<span>标签的下一个兄弟标签
        spans = soup.find_all('span', class_='icon')
        for span in spans:
            if span.find('i', class_='fas fa-file-archive'):
                file_name = span.find_next_sibling('span', class_='m-l-xs').text.strip()

                archive_url = explorer_url + "/" + file_name
                print("正在处理 " + archive_url)
                
                driver.get(archive_url)
                time.sleep(TIME_DELAY)

                archive_page_source = driver.page_source

                # 使用BeautifulSoup解析
                archive_soup = BeautifulSoup(archive_page_source, 'html.parser')

                # 查找所有包含fas fa-file-archive图标的<span>标签的下一个兄弟标签
                archive_spans = archive_soup.find_all('span', class_='icon')
                for archive_span in archive_spans:
                    if archive_span.find('i', class_='fas fa-file-audio'):
                        mp3_file_name = archive_span.find_next_sibling('span').text.strip()
                        # https://bestdori.com/assets/jp/sound/scenario/bgm/00_muon_rip/00_Muon.mp3
                        mp3_url = explorer_url.replace("tool/explorer/asset/",
                                                       "assets/") + "/" + file_name + "_rip/" + mp3_file_name
                        mp3_urls.append(mp3_url)
                # 测试
                # break


def download_mp3(mp3_urls):
    for url in mp3_urls:
        filename = url.split("/")[-1]
        filepath = os.path.join(out_path, filename)
        if os.path.exists(filepath):
            print("跳过 " + url)
            continue

        try:
            print("正在下载 " + url)
            time.sleep(0.1)
            response = None
            if proxies:
                response = requests.get(url, stream=True, proxies=proxies)
            else:
                response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                break
        except Exception:
            print("请求失败，重试")
            time.sleep(TIME_DELAY)


if __name__ == '__main__':
    mp3_urls = []
    get_mp3_urls(mp3_urls)
    download_mp3(mp3_urls)
