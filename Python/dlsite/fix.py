#coding:utf-8
import os
currentPath = u"G:/音声/御崎ひより/"
dirList = os.listdir(currentPath)

for dir in dirList:
    oldDir = (currentPath + r"/" + dir)
    newDir = currentPath + dir.replace(u"╱",u"／").replace(u"⚹",u"＊").replace(u"〈",u"＜").replace(u"〉",u"＞")
    if dir[:2].lower() == "rj":
        os.rename(oldDir,newDir)
        print newDir