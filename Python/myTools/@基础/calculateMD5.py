#coding:utf8
import hashlib

filePath = r"D:\Program Files\7-Zip\7zFM.exe"

def calMD5(filePath):
    m = hashlib.md5()
    with open(filePath,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象
    return m.hexdigest()

def cal256MD5(filePath):
    m256 = hashlib.md5()
    with open(filePath,'rb') as fobj:
        data = fobj.read(256*1024)
        m256.update(data)  #更新md5对象
    return m256.hexdigest()

print(calMD5(filePath))
print(cal256MD5(filePath))

input()