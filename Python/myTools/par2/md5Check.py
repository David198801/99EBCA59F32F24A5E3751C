import os
import subprocess
import shutil
import re
import sqlite3
import hashlib
import time



inPath = r"F:\p"
outPath = r"."
md5FileName = "1600p.db"
commitSize = 100

if not inPath.endswith(os.path.sep):
    inPath+=os.path.sep

md5Path = os.path.join(outPath,md5FileName)

conn = sqlite3.connect(md5Path)
txt = open("md5Check.txt","w",encoding="utf8")

def calMD5(filePath):
    m = hashlib.md5()
    with open(filePath,'rb') as fobj:
        while True:
            data = fobj.read(81920)
            if not data:
                break
            m.update(data)  #更新md5对象
    return m.hexdigest()

try:
    
    c = conn.cursor()
    cSelect = conn.cursor()
    
    for root,dirs,files in os.walk(inPath):
        for f in files:
            filePath = os.path.join(root,f)
            PATH = filePath.replace(inPath,"")
            result = c.execute("select MD5 from T_MD5 where PATH=?",(PATH,))
            MD5 = ""
            for row in result:
                MD5 = row[0]
            if len(MD5)>0:
                if calMD5(filePath) == MD5:
                    print("[OK] " + filePath)
                else:
                    err = "[FALURE] " + filePath
                    print(err)
                    txt.write(err + "\n")
            else:
                err = "[NO RECORD] " + filePath
                print(err)
                txt.write(err + "\n")
            txt.flush()
    print("[done]")
except Exception as e:
    print(e)
    txt.write(str(e) + "\n")
finally:
    txt.close()
    conn.close()
    
