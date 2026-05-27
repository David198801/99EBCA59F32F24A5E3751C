#coding:utf-8
import os

currentPath = os.path.dirname(__file__)
fileList = os.listdir(currentPath)
dirList = os.path.split(currentPath)

print currentPath


for file in fileList:
    if file[-2:] != "py":
        oldName = currentPath + "\\" + file
        filePartL = file.split(".")
        newName = currentPath + "\\" + filePartL[0] + " " + dirList[1] + "." + filePartL[1]
        os.rename(oldName, newName)

input()