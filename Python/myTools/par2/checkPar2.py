import os
import subprocess
import shutil
import re

inPath = r"H:\f"
outPath = r"I:\p"

txt = open("checkPar2.txt","w",encoding="utf8")
for root,dirs,files in os.walk(inPath):
    for f in files:
        inFilePath = os.path.join(root,f)
        parFilePath = inFilePath.replace(inPath,outPath)+".par2"
        # print(parFilePath)
        if not os.path.exists(parFilePath):
            txt.write(inFilePath+"\n")
txt.close()