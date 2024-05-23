#检查par2文件是否有对应的源文件
import os
import subprocess
import shutil
import re

inPath = r"G:\f"
outPath = r"F:\p"

par2Set = set()
fileSet = set()
result = []

rex = re.compile(r".+\.vol\d+\+\d+\.par2$")

txt = open("checkPar2.txt","w",encoding="utf8")
for root,dirs,files in os.walk(inPath):
    for f in files:
        inFilePath = os.path.join(root,f).replace(inPath,"")
        fileSet.add(inFilePath)
        
for root,dirs,files in os.walk(outPath):
    for f in files:
        if f.endswith(".par2") and (not re.match(rex,f)):
            outFilePath = os.path.join(root,f)[:-5].replace(outPath,"")
            par2Set.add(outFilePath) 


for i in par2Set:
    if i not in fileSet:
        result.append(i)

result = sorted(result)
for i in result:
    txt.write(i+"\n")
txt.close()