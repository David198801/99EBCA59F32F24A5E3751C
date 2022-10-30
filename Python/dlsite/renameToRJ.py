import os
import re
import shutil

path = r"D:\BaiduNetdiskDownload\和鸣++++\PW：rainkmc\aaa"
comp = os.listdir(path)


rex = re.compile(r".*((RJ|rj)[0-9]{6}).*")

duplicate = os.path.join(path,"重复_自")
if not os.path.exists(duplicate):
    os.makedirs(duplicate)


for i in comp:
    rjCodeM = rex.match(i)

    if rjCodeM:
        rjCode = rjCodeM.group(1)

        oldName = os.path.join(path, i)
        if os.path.isdir(oldName):
            newName = os.path.join(path, rjCode)
        else:
            ext = i.split(".")[-1]
            newName = os.path.join(path, rjCode + "." + ext)
        if oldName != newName:
            if os.path.exists(newName):
                shutil.move(oldName,os.path.join(duplicate,i))
            else:
                os.rename(oldName, newName)
