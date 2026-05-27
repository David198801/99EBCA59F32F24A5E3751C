import os
import shutil
import subprocess

number = 2
path = r"D:\P\Aria2\Download\分片"
outPath = os.path.join(path,'out')
if not os.path.exists(outPath):
    os.makedirs(outPath)
ext = 'flv'

fileList = sorted(os.listdir(path))

partDict = {}

preName = ''
for fileName in fileList:
    filePath = os.path.join(path,fileName)
    if fileName.split(".")[-1] == ext:
        fullVideoName = fileName[:-7 - number]
        if fullVideoName == preName[:-7 - number]:
            partDict[fullVideoName].append(filePath)
        else:
            partDict[fullVideoName] = []
            partDict[fullVideoName].append(filePath)
        
        preName = fileName
    elif os.path.isfile(filePath):
        newPath = os.path.join(outPath,fileName)
        shutil.move(filePath,newPath)

txtPath = os.path.join(path,'temptxt.txt')
logPath = os.path.join(outPath,'log.log')
log = open(logPath,'w',encoding='utf-8')
for i in partDict:
    if len(partDict[i])>1:
        with open(txtPath,'w',encoding='utf-8') as txt:
            writeList = ["file \'" + x + "\'\n" for x in partDict[i]]
            txt.writelines(writeList)
            log.writelines(writeList)
            log.write("-----------------------\n")
        outName = os.path.join(outPath,i+'.'+ext)
        cmd = ['ffmpeg','-f','concat','-safe','0','-i',txtPath,'-c','copy',outName]
        subprocess.call(cmd)
        os.remove(txtPath)
    else:
        filePath = partDict[i][0]
        fileName = os.path.basename(filePath)
        newPath = os.path.join(outPath,fileName)
        shutil.move(filePath,newPath)
log.close()