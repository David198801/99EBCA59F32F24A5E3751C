# coding:utf8
import os

name = u"伊ヶ崎綾香"
path = u"G:/音声/" + name + u"/"
workType = u"音声"
txtPath = u"G:/音声/list/" + name + u"_" + workType + u".txt"

fileList = os.listdir(path)

with open(txtPath,"r") as txt:
    codeList = txt.read().splitlines()

for file in fileList:
    if file[:2]=="RJ":
        if not file[:8] in codeList:
            print(file)