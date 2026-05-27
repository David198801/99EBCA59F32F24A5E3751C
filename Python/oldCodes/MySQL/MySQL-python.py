import MySQLdb
db=MySQLdb.connect("localhost",'root','root','mysql')
cursor = db.cursor()
cursor.execute('''SELECT * FROM user;
''')
for i in range(3):
    print cursor.fetchone()