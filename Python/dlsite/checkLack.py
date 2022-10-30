# coding:utf8
import os

# name = u"御崎ひより"
# name = u"藤堂れんげ"
# name = u"餅よもぎ"
name = u"一之瀬りと"
# name = "秋野かえで"
name = "小春日より"
name = "猫乃緒みみ"

disk = 'E'

path = disk  + ":/音声/" + name + u"/"
workType = u"ボイス・ASMR"
txtPath = disk  + ":/音声/list/" + name + u"_" + workType + u".txt"
daocaowuPath = disk  + ":/音声/道草屋/"
exexceptionPath = disk  + ":/音声/" + name + u"/exception.txt"

if not os.path.exists(exexceptionPath):
    with open(exexceptionPath,"w"):
        pass

fileList = os.listdir(path)
dList = os.listdir(daocaowuPath)

def checkRJ(fileList):
    for fileNum in range(len(fileList))[::-1]:
        if fileList[fileNum][:2] == "RJ":
            fileList[fileNum] = fileList[fileNum][:8]
        else:
            del fileList[fileNum]

checkRJ(fileList)
checkRJ(dList)

with open(txtPath,"r") as txt:
    rjList = txt.readlines()

all = len(rjList)

with open(exexceptionPath,"r") as txt:
    exList = txt.readlines()
for e in range(len(exList)):
    exList[e] = exList[e][:8]

for rjNum in range(len(rjList))[::-1]:
    rj = rjList[rjNum][:-1]
    if rj in dList:
        print("道草屋:",rj)
        del rjList[rjNum]
    if rj in fileList or rj in exList:
        del rjList[rjNum]

print("总数:",all)
print("缺:",len(rjList))

with open(path + u"lack_" + workType + u".txt","w") as lack:
    for rj in rjList:
        lack.write(rj)