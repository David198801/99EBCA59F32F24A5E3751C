import json
import multiprocessing
from multiprocessing.pool import ThreadPool

import requests
from pyquery import PyQuery as pq
from urllib.parse import urljoin
import logging
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://ssr1.scrape.center/'
TOTAL_PAGE_NUM = 10
OUTPUT_DIR = r"D:\code\py"

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s: %(message)s')

def scrape_page(url):
    logging.info("正在请求:" + url)
    try:
        r = requests.get(url=url, verify=False)
        if r.status_code == 200:
            return r.text
        else:
            logging.error("响应状态不正常，响应码:"+r.status_code)
    except requests.RequestException:
        logging.error("请求发生异常，url:%s",url,exc_info=True)

def get_detail_urls(page_url):
    detail_urls = []
    resp = scrape_page(page_url)
    doc = pq(resp)
    name_pq = doc.find('.el-card.item.m-t.is-hover-shadow a.name')
    for j in name_pq:
        relative_url = pq(j).attr("href")
        detail_urls.append(urljoin(BASE_URL,relative_url))
    return detail_urls


def legal_name(name):
    return name.replace("/", u"／").replace("\\", u"＼").replace("?", u"？").replace("*", u"＊").replace("|", u"｜") \
        .replace(":", u"：").replace("<", u"＜").replace(">", u"＞").replace('''"''', u'''＂''')


def get_detail(detail_url):
    resp = scrape_page(detail_url)
    doc = pq(resp)
    name = doc("h2.m-b-sm").text()
    publish_time = doc("div.m-v-sm.info:eq(1)").text().split(" ")[0]
    describe = doc("div.drama>p").text()
    img_url = doc("div.el-card__body a>img").attr("src")
    data = {
        "name":name,
        "publish_time":publish_time,
        "describe":describe,
        "img_url":img_url
    }
    file_name = os.path.join(OUTPUT_DIR,legal_name(name)+".json")
    json.dump(data,open(file_name,"w",encoding="UTF-8"),ensure_ascii=False,indent=2)


def main():
    pool = ThreadPool(os.cpu_count())
    for i in range(1, TOTAL_PAGE_NUM + 1):
        page_url = urljoin(BASE_URL, 'page/')
        page_url = urljoin(page_url, str(i))
        detail_urls = get_detail_urls(page_url)
        for detail_url in detail_urls:
            pool.apply_async(get_detail, (detail_url,))
    pool.close()
    pool.join()
    print("Sub-process(es) done.")


if __name__ == '__main__':
    main()
