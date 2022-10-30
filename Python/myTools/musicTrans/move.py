#coding:utf8
import os
import shutil

path = r'D:\music\qaac320'
ext = 'm4a'

musicPath = r"D:\music"
flacPath  = os.path.join(musicPath,'flac')

for root,dirs,files in os.walk(flacPath):
    for f in files:
        fileExt = f.split('.')[-1]
        outFileName = f.replace(fileExt,ext)
        
        filePath = os.path.join(root,f)
        outDir = os.path.dirname(filePath.replace(flacPath,path))
        
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        
        inPath = os.path.join(path,outFileName)
        outPath = os.path.join(outDir,outFileName)
        
        print(outPath)
        shutil.move(inPath,outPath)