#coding:utf8
import os
import requests
from bs4 import BeautifulSoup

path = r"D:\BDownload\和鳴るせ"

maxSize = 1.2
minSize = 0.8

def getDirSize(path):
    size = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size

def getWebSize(RJcode):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    url = "https://www.dlsite.com/maniax/work/=/product_id/" + RJcode
    while True:
        try:
            page = requests.post(url, headers=headers,timeout=5)
            break
        except:
            continue
    soup = BeautifulSoup(page.text, features="lxml")
    folderLableList = soup.find_all(name='th',text=u"ファイル容量")
    trLable = folderLableList[0].find_parents("tr")
    s = trLable[0].td.div.string
    s = "".join([i if ord(i) < 128 else '' for i in s])
    s = s.replace("\n","")
    return s

def MB2B(s):
    if s[-2:] == "MB":
        return float(s[:-2])*1048576
    elif s[-2:] == "GB":
        return float(s[:-2])*1073741824

def checkS(RJcode,dirSize):
    w = getWebSize(RJcode)
    webSize = MB2B(w)
    ratio = dirSize/webSize
    if ratio < minSize or ratio > maxSize:
        if dirSize>1073741824:
            d = dirSize/1073741824.0
            d = '%.2fGB' % d
        elif dirSize>1048576:
            d = dirSize/1048576.0
            d = '%.2fMB' % d
        else:
            d = dirSize
        print(RJcode,"web:",w,"dir:",d)
    else:
        print(RJcode)

fileList = os.listdir(path)

for file in fileList:
    if file[:2] == "RJ":
        rj = file[:8]
        s = getDirSize(os.path.join(path, file))
        try:
            checkS(rj,s)
        except:
            print("ERROR AT " + rj)