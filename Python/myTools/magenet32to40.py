#coding:utf8
import base64

magnetPrefix = r"magnet:?xt=urn:btih:"

def magnet32to40(s):
    b32Hash = s.replace(magnetPrefix,'')
    b16Hash = base64.b16encode(base64.b32decode(b32Hash))
    b16Hash = b16Hash.lower()
    return magnetPrefix + b16Hash.decode()
    
    
def magnet40to32(s):
    b16Hash = s.replace(magnetPrefix,'')
    b32Hash = base64.b32encode(base64.b16decode(b16Hash))
    return magnetPrefix + b16Hash.decode()



txtPath = r'C:\Users\Administrator\Desktop\aaa.txt'
outPath = txtPath.replace('.txt','') + '_40.txt'
with open(txtPath,'r') as txt:
    magnetList = [x.replace('\n','') for x in txt.readlines()]
outList = []
for i in magnetList:
    outList.append(magnet32to40(i))
    
with open(outPath,'w') as txt:
    for i in outList:
        txt.write(i+'\n')
        print(i)