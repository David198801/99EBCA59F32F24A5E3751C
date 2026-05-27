import os
import shutil


path = r"D:\BaiduNetdiskDownload\伊ヶ崎綾香「99作」"

path2 = r"E:\音声\伊ヶ崎綾香"
l = os.listdir(path)
#l2 = [x[:8] for x in os.listdir(path2)]
l2 = os.listdir(path2)

duplicate = os.path.join(path, "重复_异")
if not os.path.exists(duplicate):
    os.makedirs(duplicate)

duplicateDelete = os.path.join(path, "重复_删")
if not os.path.exists(duplicateDelete):
    os.makedirs(duplicateDelete)

def getPathSize(path):
    size = 0
    if os.path.isfile(path):
        size += os.path.getsize(path)
    else:
        for root, dirs, files in os.walk(path):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
    return size

for i in l:
    rjCode = i[:8]
    for x in l2:
        j = x[:8]
        if rjCode==j:
            oldPath = os.path.join(path,i)
            duplicatePath = os.path.join(duplicate, i)
            deletePath = os.path.join(duplicateDelete, i)

            oldSize = getPathSize(oldPath)
            duplicateSize = getPathSize(os.path.join(path2, x))
            ratio = float(oldSize) / float(duplicateSize)
            if ratio < 1.2:
                shutil.move(oldPath, deletePath)
                print("delete：",oldPath, end=" ")
            else:
                shutil.move(oldPath, duplicatePath)
                print("move：", oldPath, end=" ")
            print(ratio, oldSize, duplicateSize)