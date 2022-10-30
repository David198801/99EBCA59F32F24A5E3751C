import os

path = r"D:\linshi\新建文件夹"
outName = "merge.txt"
l = os.listdir(path)
s = set([])
for i in l:
    if i[-3:]=="txt":
        with open(os.path.join(path,i),"r") as txt:
            j = txt.readline()
            while j:
                s.add(j[:-1])
                j = txt.readline()

with open(os.path.join(path, outName), "w") as txt:
    for i in s:
        txt.write(i+"\n")