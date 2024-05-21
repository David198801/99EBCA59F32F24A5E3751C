#coding:utf-8
import os

baseUrl = r"http://192.168.100.238/svn/acssvn/Control/dev/Project R & D/PRL/01.主干版本/2021/ACS_5.0.6_SYSSPLIT_20210531001.r/src/core/fundacc/"
basePath = r"D:\yss\temp0531"
if not os.path.exists(basePath):
    os.makedirs(basePath)

with open(r"C:\Users\LiuZhongbin\Desktop\scripts\batchCheckout\urls.txt","r",encoding="utf-8") as txt:
    l = [x.replace("\n","") for x in txt.readlines()]
    for i in l:
        url = i
        relativePath = url.replace(baseUrl,"")
        path = os.path.join(basePath,relativePath)
        if os.path.exists(path):
            command = 'svn update ' + path
        else:
            command = 'svn checkout "' + url + '" ' + path
        print(command)
        os.system(command)