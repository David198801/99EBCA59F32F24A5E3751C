import os
import shutil

path = r"D:\BaiduNetdiskDownload\小春日"
noncomp = os.path.join(path,"noncomp")
if not os.path.exists(noncomp):
    os.makedirs(noncomp)


compExtList = ["mp3","wav","flac","aac"]

def checkComExt(workPath):
    for root,dirs,files in os.walk(workPath):
        for f in files:
            ext = f.split(".")[-1]
            for e in compExtList:
                if e == ext:
                    return True

l = os.listdir(path)
for i in l:
    workPath = os.path.join(path,i)
    if checkComExt(workPath):
        old = workPath
        new = os.path.join(path,noncomp,i)
        shutil.move(old,new)