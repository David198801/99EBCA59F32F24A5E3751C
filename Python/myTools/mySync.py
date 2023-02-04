#coding:utf8
import os
import time
import shutil

activePath = r"C:\Users\LiuZhongbin\Desktop\scripts\mySync\com.yss.acs.third.cqrcb"
backupPath = r"C:\Users\LiuZhongbin\Desktop\scripts\mySync\cqrcb"
isSoftDelete = True
winrarPath = ""
timeflag = str(int(time.time()))
softDirName = "delete"+timeflag

def checkAndCreateDir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("create",path)

def isEmpty(dirPath):
    return not os.listdir(dirPath)
    
def softDelete(deletePath,targetPath):
    deleteBasePath = os.path.dirname(targetPath)
    checkAndCreateDir(deleteBasePath)
    if not os.path.exists(targetPath):
        shutil.move(deletePath,deleteBasePath)

def delete(src,dst,paths):
    softPath = os.path.join(dst,softDirName)
    for i in paths:
        deletePath = os.path.join(dst,i)
        if os.path.exists(deletePath):
            if isSoftDelete:
                deleteBasePath = os.path.dirname(os.path.join(softPath,i))
                softDelete(deletePath,deleteBasePath)
            else:
                os.remove(deletePath)
            print("delete",deletePath)
        
def deleteDir(src,dst,paths):
    softPath = os.path.join(dst,softDirName)
    for i in paths:
        deletePath = os.path.join(dst,i)
        if os.path.exists(deletePath):
            if isSoftDelete:
                targetPath = os.path.join(softPath,i)
                softDelete(deletePath,targetPath)
            else:
                shutil.rmtree(deletePath)
            print("deleteDir",deletePath)
    
def copy(src,dst,paths):
    for i in paths:
        srcPath = os.path.join(src,i)
        dstPath = os.path.join(dst,i)
        shutil.copy2(srcPath,dstPath)
        print("copy",i)
        
def copyDir(src,dst,paths):
    for i in paths:
        dstPath = os.path.join(dst,i)
        checkAndCreateDir(dstPath)
        

def process(src,dst):
    if not os.path.exists(src):
        print("源目录不存在")
        return
    srcRelativePaths = set()
    dstRelativePaths = set()
    srcDirRelativePaths = set()
    dstDirRelativePaths = set()
    for root, dirs, files in os.walk(src):
        for file in files:
            filePath = os.path.join(root,file)
            srcRelativePaths.add(filePath.replace(src+"\\",""))
        for d in dirs:
            dirPath = os.path.join(root,d)
            srcDirRelativePaths.add(dirPath.replace(src+"\\",""))
    for root, dirs, files in os.walk(dst):
        for file in files:
            filePath = os.path.join(root,file)
            dstRelativePaths.add(filePath.replace(dst+"\\",""))
        for d in dirs:
            dirPath = os.path.join(root,d)
            dstDirRelativePaths.add(dirPath.replace(dst+"\\",""))
    copyDirRelativePaths = sorted(srcDirRelativePaths - dstDirRelativePaths,key = lambda i:len(i),reverse=True)
    deleteDirRelativePaths = sorted(dstDirRelativePaths - srcDirRelativePaths,key = lambda i:len(i))
    if isSoftDelete and deleteDirRelativePaths:
        softPath = os.path.join(dst,softDirName)
        checkAndCreateDir(softPath)
    copyDir(src,dst,copyDirRelativePaths)
    deleteDir(src,dst,deleteDirRelativePaths)
    
    copyRelativePaths = sorted(srcRelativePaths - dstRelativePaths)
    deleteRelativePaths = sorted(dstRelativePaths - srcRelativePaths)
    copy(src,dst,copyRelativePaths)
    delete(src,dst,deleteRelativePaths)
        
def backup():
    process(activePath,backupPath)
    
def restore():
    pass

def main():
    action = sys.argv[1]
    if action=="backup":
        backup()
    elif action=="restore":
        restore()
#main()
backup()