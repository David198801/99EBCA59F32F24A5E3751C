import os
import re

path = r"D:\music\1699"


fileList = os.listdir(path)
fill = len(str(len(fileList)))
for fileName in fileList:
    filePath = os.path.join(path,fileName)
    ext = fileName.split('.')[-1]
    pureName = fileName.replace('.'+ext,'')
    nameNum = re.search('\d+',pureName).group()
    fillNum = nameNum.zfill(fill)
    newFileName = pureName.replace(nameNum,fillNum) + '.' + ext
    newFilePath = os.path.join(path,newFileName)
    print(filePath)
    print(newFilePath)
    os.rename(filePath,newFilePath)