#coding:utf-8
import os
path = os.path.dirname(__file__).decode("gbk")
fileList = os.listdir(path)
# for file in fileList:
#     if file[:2]=="RJ":
#         if file[-2:] == "7z":
#             os.rename(path + file, path + file[:8] + file[-3:])
#         else:
#             os.rename(path + file,path + file[:8] + file[-4:])
for file in fileList:
    if file[:2]=="RJ":
        oldPath = os.path.join(path,file)
        newPath = os.path.join(path,file[:8])
        os.rename(oldPath,newPath)