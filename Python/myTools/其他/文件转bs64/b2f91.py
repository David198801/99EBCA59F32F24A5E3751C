#coding:UTF-8
import base91
import os

inDir = "./b"
outDir = "./f"
if not os.path.exists(inDir):
    os.makedirs(inDir)
if not os.path.exists(outDir):
    os.makedirs(outDir)

filenames = os.listdir(inDir)
for filename in filenames:
    inPath = os.path.join(inDir,filename)
    b=open(inPath,'r')
    outPath = os.path.join(outDir,filename[:-4])
    f=open(outPath,'wb')
    fBytes=base91.decode(b.read())
    f.write(fBytes)
    b.close()
    f.close()


