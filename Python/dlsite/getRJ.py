import os
import re
import requests
from bs4 import BeautifulSoup
import difflib

path = r"D:\BaiduNetdiskDownload\和鳴るせ\新建文件夹"
l = os.listdir(path)

rex = re.compile(r".*((\[[^(\[|\])]+\])|(\([^(\(|\))]+\))).*")
rexRJ = re.compile(r".+id\/(.{8})\.html")

headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 QIHU 360EE"}

def getName(url):

    while True:
        try:
            page = requests.get(url, headers=headers, timeout=5)
            break
        except:
            continue
    soup = BeautifulSoup(page.text, features="lxml")
    folderLableList = soup.find_all(name='a', href=re.compile("^https://www.dlsite.com/.+/work/=/product_id.*"),
                                    itemprop="url")
    name = folderLableList[0].string
    return name


for file in l:
    fileName = file.split(".")
    ext = fileName[-1]
    fileName = fileName[0]
    pureName = fileName
    while True:
        a = rex.match(pureName)
        if a:
            pureName = pureName.replace(a.group(1), "")
        else:
            break
    url = r"https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/keyword/" + \
          pureName + r"/order%5B0%5D/trend/per_page/30/from/fs.header"

    while True:
        try:
            page = requests.get(url,headers=headers,timeout=5)
            break
        except:
            continue

    soup = BeautifulSoup(page.text, features="lxml")
    resultList = soup.find_all("div",id="search_result_list")

    if resultList:
        result = resultList[0]
        aLink = result.find_all("a", class_="work_thumb_inner")[0]
        urlRJ = aLink["href"]
        print(urlRJ)

        nameRJ = getName(urlRJ)

        ratio = difflib.SequenceMatcher(None, nameRJ, pureName).quick_ratio()

        if (ratio > 0.7) or (pureName in nameRJ):
            rjCode = rexRJ.match(urlRJ).group(1)
            oldPath = os.path.join(path,file)
            newFileName = rjCode + "." + ext
            newPath = os.path.join(path,newFileName)
            if os.path.exists(newPath):
                print("已存在：",rjCode,file)
            else:
                os.rename(oldPath, newPath)
        else:
            print(nameRJ)
            print(pureName)
            print(ratio)



    else:
        print("无结果：" + fileName)



