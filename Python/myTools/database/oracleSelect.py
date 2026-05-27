#coding:utf8
import cx_Oracle


# 创建数据库链接
db = cx_Oracle.connect('aaa/aaa@127.0.0.1:1521/orcl')

cursor = cx_Oracle.Cursor(db) # db作为参数传递给函数

print("Oracle数据库版本：", db.version)
data = cx_Oracle.Cursor.execute(cursor, 'select * from t_user' )
data2 = cursor.fetchall()

# 结果为tuple类型元祖数据，下面的语句可以打印类型和数据。其他操作都是类似的了
print(type(data2))
print(data2)

# 正常关闭游标和连接，对于udpte insert等操作，还需要进行commit()操作
# cursor.close()
# db.commint()
# db.close