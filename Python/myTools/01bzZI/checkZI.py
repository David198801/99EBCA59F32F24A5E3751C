#coding:utf-8
import os

path = r"D:\linshi\ZIpng"
outPath = r"C:\Users\Administrator\Desktop\ZI.txt"
outStrList = ["{"]

l = os.listdir(path)

pngList = []
txtList = []

for i in l:
    if i.split(".")[-1] == "png":
        pngList.append(i)
    if i.split(".")[-1] == "txt":
        txtList.append(i)

def check(png):
    for j in txtList:
        if png in j:
            elem = "'"+i+"':'"+j.split(".")[-2]+"'"
            print(elem)
            outStrList.append(elem + ",") 
            return True

noneList = []
for i in pngList:
    if not check(i):
        noneList.append(i)
        
print("\n\n---------未标识--------")
for i in noneList:
    open(os.path.join(path,i+".txt"),"w").close()
    print(i)
    
outStrList[-1] = outStrList[-1][:-1] + "}"
outTxt = open(outPath,"w",encoding="gbk")
outTxt.write("".join(outStrList)) 
outTxt.close()

input()