import os

txtPath = r"input.txt"
path = r"G:\f\Collections2"
outPath = r"output.txt"

t = set()
with open(txtPath,"r",encoding="utf8") as txt:
    t = set([x.replace("\n","") for x in txt.readlines()])

s = set()
for root,dirs,files in os.walk(path):
    for f in files:
        s.add(os.path.join(root,f))

with open(outPath,"w",encoding="utf8") as txt:
    for word in t:
        if word:
            for file in s:
                if word in file:
                    txt.write(word+", "+file+"\n")