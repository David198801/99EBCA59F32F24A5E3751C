#coding:utf-8
import os
import subprocess

basePath = "http://219.141.235.67:20080/svn/acssvn/"
replacePath = "http://219.141.235.67:20080/svn/acssvn/Control/pabank/Code/CodeSZ/"

with open("urls.txt","r",encoding="utf-8") as urls:
    for i in urls.readlines():
        s = i.replace("\n","").split("/?r=")
        if len(s)<2:
            input("url没有版本号")
        url = s[0]
        r = s[1]
        oldR = str(int(r) - 1)
        relativePath = url.replace(replacePath,"")
        outPathOld = "e:/exportTemp/修改前/" + relativePath
        outPathNew = "e:/exportTemp/修改后/" + relativePath
        if not os.path.exists(os.path.dirname(outPathOld)):
            os.makedirs(os.path.dirname(outPathOld))
        if not os.path.exists(os.path.dirname(outPathNew)):
            os.makedirs(os.path.dirname(outPathNew))
        subprocess.run(["svn","export","-r",oldR,url,outPathOld])
        subprocess.run(["svn","export","-r",r,url,outPathNew])