#coding:utf-8
w = 150
h = 270
myW = int(input("宽度="))
myH = int(input("高度="))
n = w/myW #先以w为准
myW = w
myH = n*myH
if(myH>h): #如果超出范围，以h为准，再缩小一次
    n = h/myH
    myH = h
    myW = n*myW
print("宽="+str(myW))
print("高="+str(myH))
input()