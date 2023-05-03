import os
import subprocess
import shutil
import re

inPath = r"e:\f"
outPath = r"f:\p"


par2jPath = "par2j"

txt = open("par2Check.txt","w",encoding="utf8")

for root,dirs,files in os.walk(inPath):
    for f in files:
        filePath = os.path.join(root,f)
        parPath = filePath.replace(inPath,outPath)+".par2"
        if os.path.getsize(filePath)==0:#0字节文件跳过
            print("[IGNORE] " + filePath)
            continue
        if os.path.exists(parPath):
            comdList = [par2jPath,"v","/uo","/d"+root,parPath]
            p = subprocess.run(comdList, stdout=subprocess.PIPE)
            output = p.stdout.decode("gbk","ignore")
            if "All Files Complete" in output:
                print("[OK] " + filePath)
            else:
                err = "[FALURE] " + filePath
                print(err + filePath)
                txt.write(err+"\n")
        else:
            err = "[NO RECORD] " + filePath
            print(err + filePath)
            txt.write(err+"\n")
        txt.flush()
        
txt.close()