#coding:utf-8
import os
import shutil
import requests
import re
from bs4 import BeautifulSoup

# os.system("chcp 65001")

currentPath = os.path.dirname(__file__)
# currentPath = byte(currentPath).decode("gbk")
print(currentPath)
dirList = os.listdir(currentPath)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# proxies = {
#   "http": "http://127.0.0.1:1088",
#   "https": "http://127.0.0.1:1088",
# }
def getName(rjCode):
    url = "https://www.dlsite.com/maniax/work/=/product_id/" + rjCode.upper()
    while True:
        try:
            page = requests.post(url,headers=headers,timeout=5)
            break
        except Exception as e:
            print(e)
            continue

    soup = BeautifulSoup(page.text, features="lxml")
    folderLableList = soup.find_all(name='a', href=re.compile("^https://www.dlsite.com/maniax/work/=/product_id.*"),
                                    itemprop="url")
    return folderLableList[0].string\
        .replace("/",u"／").replace("\\",u"＼").replace("?",u"？").replace("*",u"＊").replace("|",u"｜")\
        .replace(":",u"：").replace("<",u"＜").replace(">",u"＞").replace('''"''',u'''＂''')


for dir in dirList:
    oldDir = (currentPath + r"/" + dir)
    if dir[:2].lower() == "rj":
        rjCode = dir[:8]
        try:
            newDir = (currentPath + "/" + rjCode.upper() + " ") + getName(rjCode)
            # print newDir.encode("gbk","ignore")
            print(newDir)
            if not os.path.exists(newDir):
                os.makedirs(newDir)
            shutil.move(oldDir, newDir)
        except Exception as e:
            print("IN " + rjCode + str(e))