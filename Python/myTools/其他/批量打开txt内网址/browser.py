#coding:utf8
import webbrowser
import os
currentPath = os.path.dirname(__file__)
txtList = os.listdir(currentPath)
for i in txtList:
    if i.split('.')[-1]=='txt':
        with open(i,'r') as txt:
            urlList = [x.replace('\n','') for x in txt.readlines()]
            for j in urlList:
                webbrowser.open(j)
    

