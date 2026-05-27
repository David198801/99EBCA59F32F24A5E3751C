import os

path = r"E:\音声\一之瀬りと"

def checkInsideRJ(workPath,rjCode):
    for root, dirs, files in os.walk(workPath):
        for f in files:
            if rjCode in f:
                return True

l = os.listdir(path)
for dir in l:
    if dir[:2] == "RJ":
        rjCode = dir[:8]
        workPath = os.path.join(path,dir)
        if not checkInsideRJ(workPath, rjCode):
            print(workPath)
