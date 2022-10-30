import os
import shutil

daocaowuPath = r"E:\音声\道草屋"
listFile = r"E:\音声\list\御崎ひより_ボイス・ASMR.txt"

temp = os.path.join(daocaowuPath,"temp")
if not os.path.exists(temp):
    os.makedirs(temp)

with open(listFile,"r") as txt:
    l = txt.readlines()
    rjList = [x.replace("\n", "") for x in l]

dList = os.listdir(daocaowuPath)

for dDir in dList:
    if dDir[:2].upper() == "RJ":
        rjCode=dDir[:8]
        for r in rjList:
            if rjCode==r:
                oldPath = os.path.join(daocaowuPath,dDir)
                newPath = os.path.join(temp,dDir)
                shutil.move(oldPath,newPath)