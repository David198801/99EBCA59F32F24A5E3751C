#coding:utf-8
import os
import codecs
path = os.path.dirname(__file__).decode("gbk")
fileList = os.listdir(path)


with codecs.open("filelist.txt","w",encoding='utf-8') as txt:
    for file in fileList:
        if file[:2] == "RJ":
            print(file)
            txt.write(file+"\r\n")