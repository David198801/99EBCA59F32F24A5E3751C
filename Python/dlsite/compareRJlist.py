#coding:utf-8
import os
import re
import subprocess

#上传打包，正则提取RJ号并打包成rar，排除子目录中的“汉化”目录

inPath=r"G:\2022+2\音声\小花衣こっこ"
outPath=r"D:\temp\小花衣こっこ"
if not os.path.exists(outPath):
    os.makedirs(outPath)

rarPath = r"C:\Program Files\WinRAR\rar.exe"

l = os.listdir(inPath)
for i in l:
    dirPath = os.path.join(inPath,i)
    if os.path.isdir(dirPath):
        r = re.search(r"RJ(\d{8}|\d{6})",i)
        if r:
            rjCode = r.group()
            outFilePath = os.path.join(outPath,rjCode+".rar")
            compressCmd = [rarPath,"a",outFilePath,dirPath,"-ep1","-hpsouth-plus","-sfx","-rr3p",r"-x*\汉化"]
            print(dirPath)
            subprocess.run(compressCmd)
    