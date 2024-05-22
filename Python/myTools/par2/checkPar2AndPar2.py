#检查par2文件是否有对应的vol.par2文件
import os
import subprocess
import shutil
import re

inPath = r"H:\f\Collections2"
outPath = r"I:\p\Collections2"

rex = re.compile(r".+\.vol\d+\+\d+\.par2$")

par2Set = set()
par2volSet = set()

txt = open("checkPar2AndPar2.txt","w",encoding="utf8")
for root,dirs,files in os.walk(outPath):
    for f in files:
        if re.match(rex,f):
            par2volSet.add(".".join(os.path.join(root,f).split(".")[:-2]))
        else:
            par2Set.add(".".join(os.path.join(root,f).split(".")[:-1]))
print("par2Set="+str(len(par2Set)))
print("par2volSet="+str(len(par2volSet)))
for i in par2Set:
    if i not in par2volSet:
        txt.write(i.replace(outPath,inPath)+"\n")
txt.close()