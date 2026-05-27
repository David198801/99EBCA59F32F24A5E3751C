# coding:utf-8
import os
import shutil
import subprocess

path = r"D:\Downloads\(Rock) Bob Seger 35CD 1969-2013 FLAC+WV 10.5G"
outPath = r"D:\linshi2\a\(Rock) Bob Seger 35CD 1969-2013 FLAC+WV 10.5G"

'''
ysname = "道草屋"
path+= "\\"+ysname
outPath+= "\\"+ysname
'''

sizelimit = 2048 #MB
pw = "哆啦A梦"
pw = "Bob Seger"
pwSwitch = True  #密码
rr = "10"
rrSwitch = True
compLevel = "1" #设置压缩级别(0-存储...3-默认...5-最大)
compLevelSwitch = True

lockSwitch = True    #锁定
solidSwitch = True  #固实
blake2Switch =  True #使用blake2(256位)而不是crc32进行文件校验

duplicateSize = 2*1024*1024 #MB 单位字节，乘两次1024后为MB
duplicateSwitch = False #将大于duplicateSize的相同文件保存为引用，缩小体积


deletefileSwitch = True   #删除文件
shutdownSwitch = False     #关机


def getName(dirName):
    codeD = d[:2]
    # codeD = d.split(" ")[0] #空格分割
    # codeD = d.split(" ")[0][2:] # RJ号纯数字
    # codeD = d.split(" ")[0].split("-")[2]
    return codeD




compLevelParameter = ''' -m"''' + compLevel +'''"'''
pwParameter = ''' -hp"''' + pw + '''"'''
rrParameter = " -rr" + rr + "p"
sizeParameter  = " -v" + str(sizelimit) + "m"
lockParameter = " -k"
solidParameter = " -s"
blake2Parameter = " -htb"
duplicateParameter = " -oi:" + str(duplicateSize)
deletefileParameter = " -df"

if not os.path.exists(outPath):
    os.makedirs(outPath)


def getDirSize(path):
    size = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size

def getDirPathAndSize(path):
    p = {}
    for i in os.listdir(path):
        iPath = os.path.join(path,i)
        if os.path.isdir(iPath):
            s = getDirSize(iPath)
            
        else:
            s = os.path.getsize(iPath)
        p[i] = s
        print(i,s)
    return p

# os.chdir(path)

pDict = getDirPathAndSize(path)

sizeALL = 0
for d in pDict:
    sizeALL += pDict[d]
    
sizeNow = 0.0
for d in pDict:
    #sizeMB = pDict[d]/1000/1000
    sizeNow += pDict[d]
    print("----------------------------------------------------------")
    print(format(sizeNow/sizeALL,".2%"))
    print("----------------------------------------------------------")
    codeD = getName(d)

    newPath = os.path.join(outPath, codeD)
    # newDir = os.path.join(outPath, codeD)

    # 一律建立文件夹
    # os.makedirs(newDir)
    # newPath = os.path.join(outPath, codeD ,codeD)

    # #大于分卷大小才建立文件夹
    # newPath = os.path.join(outPath, codeD)
    # if sizeMB > sizelimit:
    #     os.makedirs(newDir)
    #     newPath = os.path.join(outPath, codeD, codeD)

    cmd = r'''"D:\Program Files\WinRAR\rar.exe" ''' + r'''a "''' + newPath + ".rar" +\
          '''" "''' + os.path.join(path, d) + r'''" -ep1''' + sizeParameter

    if pwSwitch:
        cmd = cmd +  pwParameter
    if rrSwitch:
        cmd = cmd +  rrParameter
    if compLevelSwitch:
        cmd = cmd + compLevelParameter
    if lockSwitch:
        cmd = cmd + lockParameter
    if solidSwitch:
        cmd = cmd + solidParameter
    if blake2Switch:
        cmd = cmd + blake2Parameter
    if duplicateSwitch:
        cmd = cmd + duplicateParameter
    if deletefileSwitch:
        cmd = cmd + deletefileParameter

    print(cmd)
    ps = subprocess.Popen(cmd)
    ps.wait()

    # if sizeMB > sizelimit:
    #     newDirList = os.listdir(newDir)
    #     if len(newDirList) == 1:
    #         import shutil
    #         fileName = newDirList[0]
    #         shutil.move(os.path.join(newDir,fileName),os.path.join(outPath,fileName))
    #         os.rmdir(newDir)

ol = os.listdir(outPath)
for of in ol:
    ofSpl = of.split(".")
    if len(ofSpl) > 2:
        ext2 = ofSpl[-2]
        if ext2[:4] == "part":
            ofName = ""
            for ofn in ofSpl[:-2]:
                ofName = ofName + ofn + "."
            ofName = ofName[:-1]
            newDir = os.path.join(outPath,ofName)
            if not os.path.exists(newDir):
                os.makedirs(newDir)
            oldPath = os.path.join(outPath,of)
            newPath = os.path.join(newDir,of)
            shutil.move(oldPath,newPath)

if shutdownSwitch:
    os.system(r"shutdown /s /t 120")