import requests
import re
import os
from bs4 import BeautifulSoup

linkTxt = r"D:\linshi\links.txt"
outPath = r"D:\linshi\ZIpng"
if not os.path.exists(outPath):
    os.makedirs(outPath)

headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Cookie":"__cfduid=d37159dde642ad53018a2755e41f6327c1589298127",
"Host":"01bz.tel",
"Proxy-Connection":"keep-alive",
"Referer":"http//01bz.tel/3/3036/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}




linkList = []
with open(linkTxt,"r") as txt:
    linkList = [x.replace("\n","").replace("https","http") for x in txt.readlines()]
hostname = "https://01bz.tel"
rex = re.compile(r"/toimg/data/.+png")
for url in linkList:
    print(url)
    while True:
        try:
            r = requests.get(url,headers = headers)
            break
        except Exception as e:
            print(e)
            continue
    r.encoding = "utf-8"

    bs = BeautifulSoup(r.text,features="lxml")
    
    imgList = bs.find_all("img",src=rex)
    print(imgList)
    
    for imgLabel in imgList:
        imgUrl = hostname + imgLabel["src"]
        fileName = imgUrl.split("/")[-1]
        filePath = os.path.join(outPath,fileName)
        if not os.path.exists(filePath):
            while True:
                try:
                    rImg = requests.get(imgUrl)
                    break
                except:
                    continue
            with open(filePath,"wb") as png:
                png.write(rImg.content)
        
