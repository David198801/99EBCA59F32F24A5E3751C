#coding:utf-8
import os
import shutil

currentPath = os.getcwd()
for i in os.listdir(currentPath):
  path = os.path.join(currentPath,i)
  testPath = os.path.join(os.path.join(path,"src"),"test")
  if os.path.exists(testPath):
    shutil.rmtree(testPath)
    print(testPath)
input("[done]")