import os
import shutil
import subprocess

rarPath = r"C:\Program Files\WinRAR\rar"
imgPackageName = "图片"

imgExts = ('dwg','xcf','jpg','jpeg','jpx','png','dwg','apng','gif','webp','cr2','tif','bmp','jxr','psd','ico','heic')

def packageImg(path):
    l = os.listdir(path)
    moveList = []
    for i in l:
        ext = ""
        s = i.split(".")
        if len(s) > 1:
            ext = s[-1]
        filePath = os.path.join(path,i)
        if os.path.isfile(filePath) and ext.lower() in imgExts:
            moveList.append(filePath)
    if len(moveList)>0:
        dirPath = os.path.join(path,imgPackageName)
        checkOrMakeDir(dirPath)
        for i in moveList:
            shutil.move(i,dirPath)
        packagePath = dirPath + ".rar"
        cmdList = [rarPath,"a",packagePath,dirPath,"-m0","-df","-ep1","-ma4 "]
        subprocess.run(cmdList)

def checkOrMakeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    with open("packageImg.txt","r",encoding='utf8') as txt:
        l = [x.replace("\n","") for x in txt.readlines()]
        for i in l:
            packageImg(i)

main()

