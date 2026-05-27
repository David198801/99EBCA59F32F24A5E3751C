import os
import shutil

path = r"D:\BaiduNetdiskDownload\哆啦A梦 日语中字 部分"

recordTxt = os.path.join(path,"record.log")

def moveUp(path):
    def recordMove(oldPath, newPath):
        txt.write(newPath + "***" + oldPath + "\n")
    txt = open(recordTxt, "w",encoding="utf8")
    listPath = os.listdir(path)
    for dirName in listPath:
        innerPath = os.path.join(path, dirName)
        if os.path.isdir(innerPath):
            for innerName in os.listdir(innerPath):
                oldPath = os.path.join(innerPath, innerName)
                newPath = os.path.join(path, innerName)
                recordMove(oldPath, newPath)
                shutil.move(oldPath, newPath)
            os.rmdir(innerPath)
    txt.close()



def undoMove(file):
    with open(file,"r",encoding="utf8") as txt:
        l = txt.readline()
        while l:
            lw = l[:-1].split("***")
            p1 = lw[0]
            p2 = lw[1]
            d = os.path.dirname(p2)
            if not os.path.exists(d):
                os.makedirs(d)
            shutil.move(p1,p2)
            l = txt.readline()

moveUp(path)
# undoMove(recordTxt)