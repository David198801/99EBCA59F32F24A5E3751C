import os

code = 'ascii'

setA = set()
setB = set()
setOut = set()
with open("A.txt",'r',encoding=code) as txtA:
    setA = set([x.replace('\n','') for x in txtA.readlines()])
with open("B.txt",'r',encoding=code) as txtB:
    setB = set([x.replace('\n','') for x in txtB.readlines()])

setOut = setA - setB

listOut = [x+"\n" for x in sorted(list(setOut))]
listOut[-1] = listOut[-1][:-1]
with open("out.txt",'w',encoding=code) as txt:
    txt.writelines(listOut)