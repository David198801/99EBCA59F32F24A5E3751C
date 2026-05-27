#coding:utf-8
import os
import shutil

currentPath = os.getcwd()
for root,dirs,files in os.walk(currentPath):
  for f in files:
    if "pom.xml"==f:
      targetPath = os.path.join(root,"target")
      if(os.path.exists(targetPath)):
        shutil.rmtree(targetPath)
        print(targetPath)
input()