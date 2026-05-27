import os,shutil

with open("files.txt","r",encoding="utf8") as txt:
    l = [x.replace("\n","") for x in txt.readlines()]
    for i in l:
        if not os.path.isfile(i):
            continue
        newPath = os.getcwd() + i[2:]
        newDir = os.path.dirname(newPath)
        if not os.path.exists(newDir):
            os.makedirs(newDir)
        shutil.copy(i,newPath)
