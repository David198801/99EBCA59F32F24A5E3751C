import os
import re
import shutil

path = r"D:\linshi\111"

rex = re.compile(r".*((RJ|rj)[0-9]{6}).*")

l = os.listdir(path)

for i in l:
    rjM = rex.match(i)
    if rjM:
        rj = rjM.group(1).upper()
        newPath = os.path.join(path,rj)
        os.makedirs(newPath)
        old = os.path.join(path,i)
        new = os.path.join(newPath,i)
        shutil.move(old,new)
        print(rj)
