#coding:UTF-8
import base91
import os

inDir = "./f"
outDir = "./b"
if not os.path.exists(inDir):
    os.makedirs(inDir)
if not os.path.exists(outDir):
    os.makedirs(outDir)

filenames = os.listdir(inDir)
for filename in filenames:
    inPath = os.path.join(inDir,filename)
    f=open(inPath,'rb')
    outPath  = os.path.join(outDir,filename+".txt")
    b=open(outPath,'w')
    b91=base91.encode(f.read())
    b.write(b91)
    b.close()
    f.close()


