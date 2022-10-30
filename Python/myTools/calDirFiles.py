import os
import shutil

path = r"H:\f"

d = {}
for root,dirs,files in os.walk(path):
    for f in files:
        if root in d:
            d[root] += 1
        else:
            d[root] = 1

l=[]
for k in d:
    l.append((d[k],k))
l.sort(key=lambda s:int(s[0]),reverse=True)

with open("out.txt","w",encoding="utf8") as txt:
    for i in l:
        txt.write(str(i[0])+"\n"+i[1]+"\n")