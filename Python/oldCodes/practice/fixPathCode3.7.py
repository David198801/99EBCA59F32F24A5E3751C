#coding:utf8
import os
path = r"C:\Users\Administrator\Downloads\Compressed\RJ138049_trial"

systemCode = "EUC_KR"
systemCode = "gbk"
originalCode = "Shift_JIS"

def fixCode(path):
    if os.path.isdir(path):
        pList = os.listdir(path)
        for i in pList:
            f = path + "/"+i
            nn = i.encode(systemCode,"ignore").decode(originalCode)
            nf = path + "/"+nn
            print(f)
            print(nf)
            print("")
            if i != nn:
                os.rename(f,nf)
            fixCode(nf)


fixCode(path)