#coding:utf-8
import os
import re
s=[]

code = "utf-8"

currentPath = os.path.dirname(__file__)
path = currentPath
l = os.listdir(path)
outPath = os.path.join(path,"output.txt")


lst=[]
for i in l:
  if i[-3:]=="txt":
    lst.append(i)

lst = sorted(lst, key=lambda x: int(re.findall(r'\d+', x)[0]))

for i in lst:
  file = os.path.join(path,i)
  with open(file,"r",encoding=code) as txt:
    li = txt.readlines()
    li = [x.replace("\n","") for x in li]
    for j in li:
      s.append(j)
        
with open(outPath,"w",encoding=code) as txt:
    writeList = [x+'\n' for x in s]
    writeList[-1] = writeList[-1][:-1]
    txt.writelines(writeList)