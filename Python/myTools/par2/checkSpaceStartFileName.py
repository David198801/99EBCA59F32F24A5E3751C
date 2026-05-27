import os
import re

inPath = r"H:\f"

blankRex = re.compile(r"^\s")

with open("checkSpaceStartFileName.txt","w",encoding="utf8") as txt:
    for root,dirs,files in os.walk(inPath):
        for f in files:
            if re.match(blankRex,f):
                path = os.path.join(root,f)
                txt.write(path+"\n")