#coding:utf-8
import os
import subprocess

name = u"御崎ひより"
# name = u"test"
path = u"E:/音声/" + name + u"/"
path = r"D:/LiSA"
def getE(path):
  return os.path.splitext(path)[-1]

for root,dirs,files in os.walk(path):
    for f in files:
        ext = getE(f).lower()[1:]
        if ext == "7z" or ext == "001":
            filePath = os.path.join(root, f)
            cmd7l = u'''7z l "''' + filePath + u'''"'''
            cmd7t = u'''7z t "''' + filePath + u'''"'''
            # cmd = '''"''' + filePath + '''"'''

            p = subprocess.run(cmd7l, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            output = p.stdout.decode("gbk","ignore")
            if "Enter password" in output:
                print(f)
            elif "7zAES" in output:
                print(f)

        elif ext == "rar":
            filePath = os.path.join(root, f)
            cmdRl = u'''rar l -p- "''' + filePath + u'''"'''
            p = subprocess.run(cmdRl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = p.stdout.decode("gbk","ignore")
            if u"已加密" in output:
                print(f)
            elif "*" in output:
                print(f)

        elif ext == "zip":
            filePath = os.path.join(root, f)
            cmdZl = u'''winzip -v "''' + filePath + u'''"'''
            p = subprocess.run(cmdZl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = p.stdout.decode("gbk","ignore")
            if "*" in output:
                print(f)
