import os
currentPath = os.path.dirname(__file__)
l = os.listdir(currentPath)
with open("dir.txt","w") as txt:
    for i in l:
        if os.path.isdir(os.path.join(currentPath,i)):
            txt.write(i+"\n")
