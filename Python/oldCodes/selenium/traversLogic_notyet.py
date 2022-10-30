import os

downloadPath = r""


rootPath = r"D:\linshi2\dir"
rootPath = r"D:\BaiduNetdiskDownload"
pathList = {rootPath:1}
level = [1]
currentPath = [""]

def download(p):
    print("download: "+p)

def enterPath(p):
    print("test: currentPath=" + currentPath[0] + ",wantPath=" + p)
    currentPath[0] = p
    print("current: " + p)

def checkLevel(l,d):
    for i in d:
        if d[i] == l:
            if os.path.isfile(i):
                return i
    for i in d:
        if d[i] == l:
            return i

while pathList:
    path = checkLevel(level[0], pathList)
    if path:
        if os.path.isfile(path):
            download(path)
            pathList.pop(path)
        elif os.path.isdir(path):
            # currentSplit = currentPath[0].split("\\")
            # pathSplit = path.split("\\")
            # if len(currentSplit) == len(pathSplit):
            #
            #     enterPath(os.path.dirname(currentPath[0]))

            enterPath(path)


            l = os.listdir(path)
            for i in l:
                absPath = os.path.join(path,i)
                pathList[absPath] = level[0] + 1
            pathList.pop(path)
    else:
        level[0] += 1