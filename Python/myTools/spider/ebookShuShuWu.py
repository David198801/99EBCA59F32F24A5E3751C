import requests
from bs4 import BeautifulSoup


bookTxt = open(r"D:\linshi2\ebook.txt","w",encoding="utf-8")


headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Cache-Control":"max-age=0",
"Cookie":"__cfduid=d2bf50b194187845e82b2199b3be7dd741589185299; jieqiVisitId=article_articleviews%3D1069",
"Host":"www.shushu5.cc",
"Proxy-Connection":"keep-alive",
"Referer":"http//www.shushu5.cc/1_1069/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}



urlList = []
with open(r"D:\linshi2\新建 文本文档.txt") as txt:
    urlList = [x.replace("\n","") for x in txt.readlines()]

for url in urlList:
    fullUrl = r"http://www.shushu5.cc" + url
    print(fullUrl)
    r = requests.get(fullUrl,headers=headers)
    r.encoding = "gbk"
    bs = BeautifulSoup(r.text,features="lxml")
    divList = bs.find_all(name="div",id="content")
    s = divList[0]
    n = 0
    for i in s:
        if i.name != "br":
            if n==0:
                i = i.replace(" ","")
            bookTxt.write(i.replace("\r\n",""))
        n += 1
        
bookTxt.close()