#coding:utf8
import os
import subprocess
import re

path = r"D:\linshi\葵"
videoExtList = ["mp4","wmv","mkv","avi"]

dirList = os.listdir(path)

rex = re.compile(r".+?(\d{3,4}x\d{3,4}).+")

def getFFmpegOut(filePath):
    command = ["ffprobe.exe", "-show_format", "-i", filePath]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = str(result.stdout.read())
    return out

def getResolution(out):
    rm = rex.match(out)
    r =  rm.group(1)
    return r


for moiveDir in dirList:
    moivePath = os.path.join(path,moiveDir)
    fileList = os.listdir(moivePath)
    for file in fileList:
        if file.split(".")[-1].lower() in videoExtList:
            filePath = os.path.join(moivePath,file)
            out = getFFmpegOut(filePath)
            resolution = getResolution(out)
            old = moivePath
            new = moivePath + " " + resolution
            os.rename(old,new)
            print(old,new)
            break
