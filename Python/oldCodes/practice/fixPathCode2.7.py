#coding:utf8
import os
path = u"C:/Users/admin/Desktop/RJ150184"

wrongCode = "cp1251"
rightCode = "Shift JIS"

def fixCode(path):
    if os.path.isdir(path):
        pList = os.listdir(path)
        for i in pList:
            f = path + "/"+i
            nn = i.encode(wrongCode,"ignore").decode(rightCode)
            nf = path + "/"+nn
            print f
            print nf
            print ""
            if i != nn:
                os.rename(f,nf)
            fixCode(nf)


fixCode(path)