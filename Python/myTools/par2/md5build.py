import os
import subprocess
import shutil
import re
import sqlite3
import hashlib
import time



inPath = r"F:\p"
outPath = r"."
md5FileName = r"1600p.db"
commitSize = 100

if not inPath.endswith(os.path.sep):
    inPath+=os.path.sep

md5Path = os.path.join(outPath,md5FileName)

conn = sqlite3.connect(md5Path)


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
    #创建表
    conn.execute('''
    CREATE TABLE IF NOT EXISTS T_MD5(
        PATH TEXT primary key,
        MD5 TEXT,
        TIME DATE
    )
    ''')

    c = conn.cursor()
    cSelect = conn.cursor()
    
    result = cSelect.execute("select PATH,TIME from T_MD5")
    for row in result:
        PATH = row[0]
        TIME = row[1]
        filePath = os.path.join(inPath,PATH)
        if ((not os.path.exists(filePath)) or (TIME<os.path.getmtime(filePath))):
            print("[delete] "+PATH)
            c.execute("delete from T_MD5 where PATH=?",(PATH,))
    conn.commit()
    
    #插入数据
    sql = "insert into T_MD5(PATH,MD5,TIME) values(?,?,?)"
    values = []
    
    for root,dirs,files in os.walk(inPath):
        for f in files:
            filePath = os.path.join(root,f)
            PATH = filePath.replace(inPath,"")
            #查询是否已存在
            c.execute("select count(1) from T_MD5 where PATH=?",(PATH,))
            if c.fetchone()[0]<1:
                print("[calMD5] "+filePath)
                values.append((PATH,calMD5(filePath),time.time()))
                if len(values)==commitSize:
                    c.executemany(sql,values)
                    conn.commit()
                    values = []
    
    if len(values)>0:
        c.executemany(sql,values)
        conn.commit()
        
    c.execute("select count(1) from T_MD5 ")
    print("总数:"+str(c.fetchone()[0]))
    input("按任意键继续")
except Exception as e:
    conn.rollback()
    print(e)
finally:
    conn.close()