#coding:utf8
import os

path = "E:\\"

def getE(path):
    return os.path.splitext(path)[-1]

def checkE(path,l):
    for root, dirs, files in os.walk(path):
        for f in files:
            e = getE(f).lower()
            if e:
                if e not in l:
                    l.append(e)
            else:
                print(f)
l = []
checkE(path,l)
l = sorted(l)
for i in l:
    print(i)
