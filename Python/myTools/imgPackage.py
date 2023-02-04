#coding:utf-8
import os
import subprocess
import shutil

rarPath = r"C:\Program Files\WinRAR\rar.exe"
baseDirPath = r"D:\temp\aa"
imgDirName = "图"

def isImg(path):
    if path and ("." in path):
        ext = path.split(".")[1]
        if ext.lower() in ["jpg","jpeg","png","bmp","gif","tif","tiff"]:
            return True
    return False

def deal(dirPath):
    l = os.listdir(dirPath)
    # 有子目录则不处理，只处理仅包含文件的目录
    for i in l:
        path = os.path.join(dirPath,i)
        if os.path.isdir(path):
            return
    imgCount = 0
    otherCount = 0
    imgList = []
    for i in l:
        path = os.path.join(dirPath,i)
        if isImg(path):
            imgCount += 1
            imgList.append(path)
        else:
            otherCount += 1
            
    if imgCount>1:
        if otherCount>0:
            imgDirPath = os.path.join(dirPath,imgDirName)
            os.makedirs(imgDirPath)
            compressPath = imgDirPath
            for i in imgList:
                shutil.move(i,imgDirPath)
        else:
            compressPath = dirPath
        compressCmd = [rarPath,"a",compressPath+".rar",compressPath,"-ep1","-df","-ma4"]
        print(compressPath)
        subprocess.run(compressCmd)

for root,dirs,files in os.walk(baseDirPath):
    for dir in dirs:
        dirPath = os.path.join(root,dir)
        deal(dirPath)