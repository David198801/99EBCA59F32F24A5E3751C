import os

path = r"E:\音声\御崎ひより"
listFile = r"E:\音声\list\御崎ひより_ボイス・ASMR.txt"
rjList = []
with open(listFile,"r") as txt:
    l = txt.readlines()
    rjList = [x.replace("\n","") for x in l]

fileList = os.listdir(path)
for dir in fileList:
    if dir[:2] == "RJ":
        rjCode = dir[:8]
        c = 0
        for r in rjList:
            if rjCode == r:
                c += 1
        if c != 1:
            print(rjCode)