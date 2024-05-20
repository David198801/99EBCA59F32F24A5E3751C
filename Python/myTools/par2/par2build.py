import os
import subprocess
import shutil
import re

inPath = r"f:\f"
outPath = r"e:\p"


par2jPath = "par2j"

# par2备份文件
rex = re.compile(r".+\.vol\d+\+\d+\.par2$")

# 删除不存在的目录
outWalkList = os.walk(outPath)
for rootO,dirsO,filesO in outWalkList:
    for dirO in dirsO:
        dirPathO = os.path.join(rootO,dirO)
        dirPathI = dirPathO.replace(outPath,inPath,1)
        if not os.path.exists(dirPathI):
            print("[delete] " + dirPathO)
            shutil.rmtree(dirPathO)

# 删除不存在的文件的par2
outWalkList = os.walk(outPath)
for rootO,dirsO,filesO in outWalkList:
    for fileO in filesO:
        if fileO.lower().endswith(".par2"):
            filePathO = os.path.join(rootO,fileO)
            if re.match(rex,fileO):
                fileI = ".".join(fileO.split(".")[:-2])
            else:
                fileI = fileO[:-5]
            filePathI = os.path.join(rootO,fileI).replace(outPath,inPath,1)
            if not os.path.exists(filePathI):
                print("[delete] " + filePathO)
                os.remove(filePathO)
                
               
def buildPar2(par2Path,filePathI):
    print("[par2Path] "+par2Path)
    print("[filePathI] "+filePathI)
    cmdList = [par2jPath,"c","/rr10","/rf1","/d"+os.path.dirname(filePathI),par2Path,os.path.basename(filePathI)]
    subprocess.run(cmdList)
    
# 创建par2
inWalkList = os.walk(inPath)
for rootI,dirsI,filesI in inWalkList:
    for fileI in filesI:
        filePathI = os.path.join(rootI,fileI)
        filePathO = filePathI.replace(inPath,outPath,1)
        par2Path = filePathO+".par2"
        if os.path.getsize(filePathI)==0:#0字节文件跳过
            continue
        if (not os.path.exists(par2Path)):
            buildPar2(par2Path,filePathI)
        else:
            #文件更新的情况
            if os.path.getmtime(par2Path)<os.path.getmtime(filePathI):
                dirPath = os.path.dirname(par2Path)
                #手动删除旧的par2文件，避免par2文件块发生变化导致没覆盖掉
                for i in os.listdir(dirPath):
                    if re.match(rex,i) and ".".join(i.split(".")[:-2])==fileI:
                        p = os.path.join(dirPath,i)
                        print("[delete] " + p)
                        os.remove(p)
                buildPar2(par2Path,filePathI)
