import requests
import re
import os
from bs4 import BeautifulSoup
outPath = r"D:\BaiduNetdiskDownload\sha1"
url = r"C:\Users\Administrator\Desktop\影片发行（资源帖必须发布于此） - 资源分享 - Secus.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

sha1LinkRex = re.compile(r".+\|[0-9]+\|\w{40}\|\w{40}")
sha1LinkInOneStrRex = re.compile(r".{1,40}\|[0-9]+\|\w{40}\|\w{40}")
txtRex = re.compile(r".+.txt")

def writeTxt(txtName,txtList):
    txtPath = os.path.join(outPath, txtName + ".txt")
    n = 1
    while os.path.exists(txtPath):
        txtPath = os.path.join(outPath, txtName + "_" + str(n) + ".txt")
        n += 1
    with open(txtPath, "w", encoding="utf8") as txt:
        for i in txtList:
            txt.write(i + "\n")

def downloadTxt(txtName,url):
    txtPath = os.path.join(outPath, txtName + ".txt")
    n = 1
    while os.path.exists(txtPath):
        txtPath = os.path.join(outPath, txtName + "_" + str(n) + ".txt")
        n += 1


def checkPtext(pText):
    nNum = 0
    for c in pText:
        if c == "\n":
            nNum += 1
        if nNum > 1:
            return True

if os.path.isfile(url):
    with open(url,"r",encoding="utf8") as html:
        soup = BeautifulSoup(html.read(),features="lxml")
        detailsList = soup.find_all("details")
        for details in detailsList:
            title = details.summary.string.replace(" ", "").replace("\n", "")
            pList = details.find_all("p")
            #if pList:
            #print("P标签数:" + str(len(pList)))
            sha1List = []
            if len(pList) == 1:
                lineList = pList[0].get_text().split("\n")
                for line in lineList:
                    cleanLine = line.replace(" ", "")
                    lineRe = sha1LinkRex.match(cleanLine)
                    if lineRe:
                        sha1 = lineRe.group(0)
                        sha1List.append(sha1)
                    else:
                        getSha1 = sha1LinkInOneStrRex.findall(cleanLine)
                        if getSha1:
                            for i in getSha1:
                                sha1List.append(i)
            else:
                for p in pList:
                    pText = p.get_text()
                    cleanLine = pText.replace(" ", "")
                    lineRe = sha1LinkRex.match(pText.replace(" ", ""))
                    if lineRe:
                        sha1 = lineRe.group(0)
                        sha1List.append(sha1)
                    else:
                        getSha1 = sha1LinkInOneStrRex.findall(cleanLine)
                        if getSha1:
                            for i in getSha1:
                                sha1List.append(i)

            if sha1List:
                writeTxt(title, sha1List)

            aList = details.find_all("a",href=txtRex)
            print("a标签数:" + str(len(aList)))
            for a in aList:
                print(a["href"])
