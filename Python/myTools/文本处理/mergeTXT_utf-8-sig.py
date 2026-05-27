import os
s = set([])

code = "utf-8-sig"

currentPath = os.path.dirname(__file__)
path = currentPath
l = os.listdir(path)
outPath = os.path.join(path,"output.txt")

for i in l:
  if i[-3:]=="txt":
    file = os.path.join(path,i)
    with open(file,"r",encoding=code) as txt:
      li = txt.readlines()
      li = [x.replace("\n","") for x in li]
      for j in li:
        s.add(j)
        
with open(outPath,"w",encoding=code) as txt:
    writeList = [x+'\n' for x in sorted(list(s))]
    writeList[-1] = writeList[-1][:-1]
    txt.writelines(writeList)