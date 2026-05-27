import os.path
import shutil

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import traceback

from get_live2d_download import store_l2d

# 代理
# proxies = None
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890',
}

LIVE2D_URL = "https://bestdori.com/tool/explorer/asset/jp/live2d/chara"

TIME_DELAY = 3

# 指定chromedriver的路径
driver_path = r'E:\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# 创建 ChromeOptions 实例 (可选)
chrome_options = Options()

# 创建浏览器驱动实例
driver = webdriver.Chrome(service=service)

# 文件输出路径
out_path = r"E:\bestdori\live2d"


def get_list(live2d_name_list):
    # 打开指定的URL
    driver.get(LIVE2D_URL)
    time.sleep(TIME_DELAY)
    page_source = driver.page_source

    # 使用BeautifulSoup解析
    soup = BeautifulSoup(page_source, 'html.parser')

    # 查找所有包含fas fa-file-archive图标的<span>标签的下一个兄弟标签
    spans = soup.find_all('span', class_='icon')
    for span in spans:
        if span.find('i', class_='fas fa-file-archive'):
            name = span.find_next_sibling('span', class_='m-l-xs').text.strip()
            live2d_name_list.append(name)

if __name__ == '__main__':

    live2d_name_list = []
    get_list(live2d_name_list)

    out_path = out_path.replace("\\", os.path.sep).replace("/", os.path.sep)

    for root,dirs,files in os.walk(out_path):
        for f in files:
            file_path = os.path.join(root,f)
            if os.path.exists(file_path) and os.path.getsize(file_path)==0:
                name = file_path.replace("\\", os.path.sep).replace("/", os.path.sep).replace(out_path,"")
                if name.startswith(os.path.sep):
                    name = name[1:]
                name = name.split(os.path.sep)[0]
                name_path = os.path.join(out_path, name)
                print("移除 "+name_path)
                shutil.rmtree(name_path)

    for name in live2d_name_list:
        if os.path.exists(os.path.join(out_path, name)) or name.endswith("_general"):
            print("跳过"+name)
            continue
        store_l2d(out_path,name)
