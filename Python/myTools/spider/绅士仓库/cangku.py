import json
import re

with open("./j.json",'r') as load_f:
  load_dict = json.load(load_f)

a = load_dict["data"]

txt = open("out.txt","w",encoding="utf-8")
for i in a:
    title = i["title"]
    
    rjCodeList = re.findall(r"\w{2}\d{6}",title,re.I)
    if rjCodeList:
        rjCodeStr = ""
        for rjCode in rjCodeList:
            rjCodeStr = rjCodeStr + rjCode + " "
        rjCodeStr = rjCodeStr[:-1]
    else:
        rjCodeStr = "无"
    txt.write(rjCodeStr+",")
    txt.write(title)
    txt.write("\n")
txt.close()