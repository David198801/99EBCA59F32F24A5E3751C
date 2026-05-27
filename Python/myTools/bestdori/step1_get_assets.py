import os.path

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By

# 是否从txt解析？
is_get_link_from_txt = True
# 是否跳过已存在？
is_pass_exists = True

# 代理
# proxies = None
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890',
}

SCENARIO_URL_S = ["https://bestdori.com/tool/explorer/asset/jp/scenario",
                  "https://bestdori.com/tool/explorer/asset/jp/characters/resourceset"]
# 测试
# SCENARIO_URL_S = ["https://bestdori.com/tool/explorer/asset/jp/characters/resourceset"]

# 排除的文件夹
EXCLUDE_DIRS = ["effects"]

TIME_DELAY = 3

# 指定chromedriver的路径
driver_path = r'E:\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# 创建 ChromeOptions 实例 (可选)
chrome_options = Options()

# 创建浏览器驱动实例
driver = webdriver.Chrome(service=service)

# 文件输出路径
assets_out_path = r"E:/bestdori/asset"
assets_txt_path = assets_out_path + "/links.txt"


def check_and_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_assets_zip_url_s(urls, assets_zip_urls):
    for url in urls:
        get_assets_zip_url(url, assets_zip_urls)


# 获取包含assets的包的路径, [{'relative_path': 'actionset/group0', 'url': 'https://bestdori.com/tool/explorer/asset/jp/scenario/actionset/group0'}]
def get_assets_zip_url(url, assets_zip_urls):
    # 打开指定的URL
    driver.get(url)
    time.sleep(TIME_DELAY)
    page_source = driver.page_source

    # 使用BeautifulSoup解析
    soup = BeautifulSoup(page_source, 'html.parser')

    # 查找所有包含fas fa-file-archive图标的<span>标签的下一个兄弟标签
    spans = soup.find_all('span', class_='icon')
    for span in spans:
        if span.find('i', class_='fas fa-file-archive'):
            file_name = span.find_next_sibling('span', class_='m-l-xs').text.strip()
            full_url = url + "/" + file_name
            assets_zip_urls.append({
                "relative_path": full_url.replace(url + "/", ""),
                "url": full_url
            })
            # 测试
            # return
        elif span.find('i', class_='fas fa-folder'):
            dir_name = span.find_next_sibling('span', class_='m-l-xs').text.strip()
            if dir_name in EXCLUDE_DIRS:
                print("跳过 " + dir_name)
            else:
                full_url = url + "/" + dir_name
                get_assets_zip_url(full_url, assets_zip_urls)


# 获取assets文件的路径{相对路径,[url1,url2]}
def get_assets_url(assets_zip_urls, assets_urls):
    for d in assets_zip_urls:
        relative_path = d['relative_path']
        print("正在处理 " + relative_path)
        assets_url = d['url']

        # 打开指定的URL
        driver.get(assets_url)
        time.sleep(TIME_DELAY)

        # 查找并点击 "Script" 标签
        try:
            # 查找 class 为 'tabs is-centered' 的 div 标签
            tabs_div = driver.find_element(By.CSS_SELECTOR, 'div.tabs.is-centered')
            # 查找文本为 "Script" 的标签（假设它是一个 <a> 标签）
            script_tab = tabs_div.find_element(By.XPATH, ".//a[text()='Script']")
            # 如果找到了这个标签，就模拟鼠标点击它
            if script_tab:
                ActionChains(driver).move_to_element(script_tab).click().perform()
                time.sleep(TIME_DELAY)  # 等待页面加载或执行 JavaScript
        except Exception as e:
            pass

        # 获取页面源代码
        page_source = driver.page_source
        # 使用 BeautifulSoup 解析页面源代码
        soup = BeautifulSoup(page_source, 'html.parser')
        # 查找所有带有 "download" 属性的 <a> 标签
        links = soup.find_all('a', attrs={'download': True})
        # 提取这些 <a> 标签的 href 属性，即链接
        asset_links = [link['href'] for link in links]
        for link in asset_links:
            full_link = 'https://bestdori.com' + link
            links = assets_urls.get(relative_path)
            if not links:
                links = []
                assets_urls[relative_path] = links
            links.append(full_link)


def record_assets(assets_urls):
    check_and_make_dir(assets_out_path)
    with open(assets_txt_path, "w", encoding="utf-8") as txt:
        for rela_path in assets_urls:
            links = assets_urls[rela_path]
            for link in links:
                txt.write(link + "\n")


def download_assets(assets_urls, is_pass_exists):
    for rela_path in assets_urls:
        dir_path = assets_out_path + "/" + rela_path
        check_and_make_dir(dir_path)

        links = assets_urls[rela_path]
        for link in links:
            filepath = os.path.join(dir_path, link.split('/')[-1])
            if is_pass_exists and os.path.exists(filepath):
                print("已存在,跳过 " + link)
                continue

            while True:
                try:
                    print("正在下载 " + link)
                    time.sleep(0.1)
                    response = None
                    if proxies:
                        response = requests.get(link, stream=True, proxies=proxies)
                    else:
                        response = requests.get(link, stream=True)
                    if response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        break
                except Exception :
                    print("请求失败，重试")
                    time.sleep(TIME_DELAY)


def get_link_from_txt(assets_urls):
    with open(assets_txt_path, "r", encoding="utf-8") as txt:
        l = [x.replace("\n", "") for x in txt.readlines()]
        for link in l:
            relative_path = link
            for i in SCENARIO_URL_S:
                u = i.replace("tool/explorer/asset/", "assets/")
                if u in relative_path:
                    relative_path = link.replace(u + "/", "")
            if "_rip" in relative_path:
                relative_path = relative_path[:relative_path.rfind('_rip')]
            elif "." in relative_path and "/" in relative_path:
                relative_path = relative_path[:relative_path.rfind('/')]

            links = assets_urls.get(relative_path)
            if not links:
                links = []
                assets_urls[relative_path] = links
            links.append(link)


def delete_latest_files(directory):
    if not os.path.exists(directory):
        print("指定的路径不存在。")
        return

    # 存储最新时间的变量和对应的文件列表
    latest_time = 0
    latest_files = []

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith("links") and file.endswith(".txt"):
                continue
            file_path = os.path.join(root, file)
            # 获取文件的创建时间
            create_time = os.path.getctime(file_path)

            # 如果发现新的最新创建时间，更新列表
            if create_time > latest_time:
                latest_time = create_time
                latest_files = [file_path]
            elif create_time == latest_time:
                # 如果是相同的创建时间，添加到列表中
                latest_files.append(file_path)

    # 删除最新创建的文件
    for file_to_delete in latest_files:
        try:
            os.remove(file_to_delete)
            print(f"删除文件: {file_to_delete}")
        except Exception as e:
            print(f"删除文件 {file_to_delete} 时出错: {e}")


if __name__ == '__main__':

    assets_urls = {}
    # 解析下载地址
    if is_get_link_from_txt and os.path.exists(assets_txt_path):
        # 直接从txt解析下载链接
        get_link_from_txt(assets_urls)
    else:
        assets_zip_urls = []
        # 解析包含下载链接的包
        get_assets_zip_url_s(SCENARIO_URL_S, assets_zip_urls)

        # 测试用，只取第一条
        # assets_zip_urls = assets_zip_urls[:1]
        # 解析下载链接
        get_assets_url(assets_zip_urls, assets_urls)

        record_assets(assets_urls)

    # 删除文件创建时间最新的文件
    delete_latest_files(assets_out_path)

    # 下载文件,跳过已存在
    download_assets(assets_urls, is_pass_exists)

# 关闭浏览器
driver.quit()
