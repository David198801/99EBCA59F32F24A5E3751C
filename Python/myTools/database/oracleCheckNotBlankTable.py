#coding:utf8
import cx_Oracle


# 创建数据库链接
db = cx_Oracle.connect('aaa/aaa@127.0.0.1:1521/orcl')

cursor = cx_Oracle.Cursor(db) # db作为参数传递给函数

print("Oracle数据库版本：", db.version)

tableNames = []
errTableNames = []
noBlankTables = []

with open('t.txt','r') as txt:
    tableNames = [x.replace('\n','') for x in txt.readlines()]

for t in tableNames:
    try:
        data = cx_Oracle.Cursor.execute(cursor, 'select count(1) from '+ t)
        data2 = cursor.fetchone()
        lineNum = data2[0]
        if(int(lineNum)>0):
            noBlankTables.append(t)
    except:
        errTableNames.append(t)


txt = open('noBlankTables.txt','w')

print('非空：')
for i in noBlankTables:
    print(i)
    txt.write(i+'\n')

print('出错：')
for i in errTableNames:
    print(i)

txt.close()