#coding:utf8
import os
import requests
from pyquery import PyQuery as pq

url1 = r"http://m.zhangyoubao.com/"

def createDir(dirName,path=""):
    path = os.path.join(path,dirName)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

with open("url.txt","r") as txt:
    for i in [x.replace("\n","") for x in txt.readlines()]:
        url=url1+i
        r = requests.get(url)
        doc = pq(r.text)
        imgs = doc("article p>img")
        title = doc("title").text()
        dirName = title.split(" ")[0]
        path = createDir(dirName=dirName)
        count = 1
        for j in imgs:
            imgUrl = pq(j).attr("data-original")
            print(imgUrl)
            fileName = str(count)+".png"
            filePath = os.path.join(path,fileName)
            ri = requests.get(imgUrl)
            if ri.status_code==200:
                with open(filePath,"wb") as jpg:
                    for chunk in ri.iter_content(chunk_size=1024):
                        jpg.write(chunk)
                count+=1