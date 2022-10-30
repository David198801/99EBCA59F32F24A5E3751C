import os

path = "E:\音声"

def checkDuplicate(li):
    l = sorted(li)
    duplicate = set([])
    for i in range(1, len(l)):
        if l[i] == l[i - 1]:
            duplicate.add(l[i])
    return duplicate

rjList = []

for dir in os.listdir(path):
    dirP = os.path.join(path, dir)
    if os.path.isdir(dirP):
        for dir2 in os.listdir(dirP):
            dir2P = os.path.join(dirP, dir2)
            if os.path.isdir(dir2P):
                if dir2[:2].lower() == "rj":
                    rjCode = dir2[:8]
                    rjList.append(rjCode)
                if dir2 == "game":
                    for dirGame in os.listdir(dir2P):
                        if dir2[:2].lower() == "rj":
                            rjCode = dir2[:8]
                            rjList.append(rjCode)


d = checkDuplicate(rjList)

for i in d:
    print(i)
