#-*-coding:utf-8-*-
import requests
import re
from bs4 import BeautifulSoup
import os
# import time

dataName = 'MOD09GA'

# def downloadFile(name, url):
#     r = requests.get(url, headers=headers, stream=True)
#     f = open(name, 'wb')
#     for chunk in r.iter_content(chunk_size=512):
#         if chunk:
#             f.write(chunk)
#     print name
#     f.close()


headers = {
        # 'Cookie': 'DATA=XH6MmMF3OXPWAHF6ldlgnAAAADA',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


dataPath = "D:/paddy/"+dataName + "/"
dataUrl = 'https://e4ftl01.cr.usgs.gov/MOLT/'+ dataName +'.006/'
if dataName[:3]=="MYD":
    dataUrl=dataUrl.replace("MOLT","MOLA")

r = requests.get(dataUrl, headers=headers)
soup = BeautifulSoup(r.text,features="lxml")
folderLableList = soup.find_all(name='a',href=re.compile("^20.+"))


configFilePath = dataPath + "config.ini"
configFile2Path = dataPath + "config2.ini"

try:
    with open(configFilePath, 'r') as configFile:
        config = configFile.read()
        if config:
            for folderNum in range(len(folderLableList)):
                if folderLableList[folderNum]['href'] == config:
                    folderLableList = folderLableList[folderNum + 1:]
                    print "begin with " + folderLableList[0].string
except:
    pass


for folder in folderLableList:
    filesUrl = dataUrl + folder.string
    r = requests.get(filesUrl, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    fileLableList = soup.find_all(name='a', href=re.compile(".+(27v05|27v06|28v05|28v06).+hdf$"))
    if not fileLableList:#缺少某天，记录并跳过
        with open(dataPath + "lack.txt", 'a') as lackFile:
            outP = "dataName" + " " + folder.string
            print outP
            lackFile.write(outP + "\n")
        continue

    try:
        with open(configFile2Path, 'r') as config2File:
            config2 = config2File.read().splitlines()
            if config2:
                for line in config2:
                    for pieceFile in fileLableList:
                        if line == pieceFile.string:
                            fileLableList.remove(pieceFile)
                            print "check " + pieceFile.string
        os.remove(configFile2Path)
    except:
        pass

    for pieceFile in fileLableList:
        fileName = pieceFile.string
        url = filesUrl + fileName
        saveDir = dataPath + folder.string[:4]
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        path = saveDir + '/' + fileName
        with open("D:/paddy/"+ dataName +"/link.txt", 'a') as t:
            t.write(url + "\n")
        # downloadFile(path, url)
        print folder.string
        with open(configFile2Path, 'a') as config2File:
            config2File.write(fileName + "\n")
    with open(configFilePath, 'w') as configFile:
            configFile.write(folder.string)