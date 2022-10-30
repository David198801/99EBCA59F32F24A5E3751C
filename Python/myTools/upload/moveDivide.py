import os
import shutil

path = r"D:\BaiduNetdiskDownload\哆啦A梦 日语中字 部分"
sizeLimit = 1 * 1024 * 1024 *1024 #GB
#sizeLimit = 51 * 1024 *1024 #MB

def getPathSize(path):
    size = 0
    if os.path.isfile(path):
        size += os.path.getsize(path)
    else:
        for root, dirs, files in os.walk(path):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
    return size

l = os.listdir(path)


def divedeFile(list):
    size = 0
    dirNum = 0
    start = 0
    end = 0
    fileListLength = len(list)
    for fileListNum in range(fileListLength):
        fileSize = getPathSize(os.path.join(path,list[fileListNum]))
        size += fileSize
        # 遇到单个大文件也正常工作
        # 遇到单个大文件时，前面部分+大文件总体积大于sizeLimit，移动前面部分（无论前面部分体积是否契合）
        # 然后size等于大文件size，下一个文件时必定大于sizeLimit，移动单个大文件，而后继续正常情况
        if size>sizeLimit:
            dirPath = os.path.join(path,str(dirNum))
            os.makedirs(dirPath)
            start = end
            end = fileListNum
            for file in list[start:end]:
                old = os.path.join(path,file)
                new = os.path.join(dirPath,file)
                shutil.move(old,new)
            dirNum += 1
            size = fileSize
        if fileListNum==fileListLength-1:
            dirPath = os.path.join(path,str(dirNum))
            os.makedirs(dirPath)
            start = end
            for file in list[start:]:
                old = os.path.join(path,file)
                new = os.path.join(dirPath,file)
                shutil.move(old,new)
    
    
divedeFile(l)
