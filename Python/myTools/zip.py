#coding:utf-8
import os
import zipfile
import sys

# 压缩目录、或文件
def zip(srcPath=None, zipFilePath=None, includeDirInZip=True):
    if not zipFilePath:
        zipFilePath = srcPath + ".zip"
    parentDir, dirToZip = os.path.split(srcPath) 
    
    # zipfile.write的第2个参数需要为相对路径，所以需要转换
    def trimPath(path):
        # 获取目录名称，前面带有\
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            # 去掉第一个字符
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)     
        return archivePath

    outFile = zipfile.ZipFile(zipFilePath, "w", compression=zipfile.ZIP_DEFLATED)

    if os.path.isdir(srcPath):
        # 目录的压缩包
        for (archiveDirPath, dirNames, fileNames) in os.walk(srcPath):           
            for fileName in fileNames:
                filePath = os.path.join(archiveDirPath, fileName)
                # write的第2个参数需要为相对路径
                outFile.write(filePath, trimPath(filePath))
            # 包含空目录
            if not fileNames and not dirNames:
                zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")          
                outFile.writestr(zipInfo, "")
    else:
        # 文件的压缩包
        outFile.write(srcPath, trimPath(srcPath))
    outFile.close()


# 解压文件
def unzip(zipFilePath, savePath=None):
    r = zipfile.is_zipfile(zipFilePath)
    if r:        
        if not savePath:
            savePath = os.path.split(zipFilePath)[0]
        fz = zipfile.ZipFile(zipFilePath, 'r')
        for file in fz.namelist():
            fz.extract(file, savePath)
    else:
        print('不是一个zip文件')


if __name__ == '__main__':
    for i in sys.argv[1:]:
        zip(i)