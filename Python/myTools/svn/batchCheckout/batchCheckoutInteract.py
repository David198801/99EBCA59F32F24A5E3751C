#coding:utf-8
import os

baseUrl = input("远程父目录：")
basePath = input("本地父目录：")
if not os.path.exists(basePath):
    os.makedirs(basePath)

while True:
    url = input("url：")
    relativePath = url.replace(baseUrl,"")
    path = os.path.join(basePath,relativePath)
    if os.path.exists(path):
        command = 'svn update ' + path
    else:
        command = 'svn checkout "' + url + '" ' + path
    print(command)
    os.system(command)