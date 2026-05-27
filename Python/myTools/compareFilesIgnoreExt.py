#coding:UTF-8
import os

path1 = r"D:\temp\flac1"
path2 = r"D:\temp\qaac256k1"



def getPathList(path):
    pathList = []
    for root,dirs,files in os.walk(path):
        for f in files:
            p = os.path.join(root,f).replace(path,"")[:-len(f.split(".")[-1])-1]
            pathList.append(p)
    return pathList
            
pathList1 = getPathList(path1)
pathList2 = getPathList(path2)

for i in pathList1:
    if i not in pathList2:
        print(i)