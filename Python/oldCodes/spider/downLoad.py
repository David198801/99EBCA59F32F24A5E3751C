#-*-coding:utf-8-*-
import requests
import re
import sys
from contextlib import closing
mainUrl='https://e4ftl01.cr.usgs.gov'
headers = {
    'Cookie': 'DATA=Wfx96pg9BGcAACCNJNoAAAAW',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s]%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep
    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info
    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        sys.stdout.write(self.__get_info()+end_str)
url = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD09A1.005/2000.02.18/MOD09A1.A2000049.h10v08.005.2006268191328.hdf'
fileName='MOD09A1.A2000049.h10v08.005.2006268191328.hdf'
r=requests.get(url,headers=headers,stream=True)
with closing(r) as response:
    chunk_size = 1024 # 单次请求最大值
    content_size = int(response.headers['content-length']) # 内容体总大小
    progress = ProgressBar(fileName, total=content_size,
                                     unit="KB", chunk_size=chunk_size, run_status=u"正在下载", fin_status=u"下载完成")
    with open(fileName, "wb") as file:
       for data in response.iter_content(chunk_size=chunk_size):
           file.write(data)
           progress.refresh(count=len(data))