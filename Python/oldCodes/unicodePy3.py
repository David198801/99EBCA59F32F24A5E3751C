#coding:utf8


str = r'\xe4\xbd\xa0\xe5\xa5\xbd'
c = str.encode().decode('unicode-escape').encode('raw_unicode_escape').decode('utf-8')
c2 = str.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
print(c,c2)
#.encode().decode('unicode-escape')后实际上等于恢复了\的转义
a = str.encode().decode('unicode-escape')
print(a=='\xe4\xbd\xa0\xe5\xa5\xbd')

x = r"\xe4\xbd\xa0\xe5\xa5\xbd\x31\x31\x32\x32\x62\xe6\x88\x91\xe5\xa5\xbd"
print(x.encode().decode("unicode_escape").encode("latin1").decode("utf8"))
x = r'\xe4\xbd\xa0\xe5\xa5\xbd1122b\xe6\x88\x91\xe5\xa5\xbd'
print(x.encode().decode("unicode_escape").encode("latin1").decode("utf8"))
x = "\xe4\xbd\xa0\xe5\xa5\xbd\x31\x31\x32\x32\x62\xe6\x88\x91\xe5\xa5\xbd"
print(x.encode("latin1").decode("utf8"))
x = '\xe4\xbd\xa0\xe5\xa5\xbd1122b\xe6\x88\x91\xe5\xa5\xbd'
print(x.encode("latin1").decode("utf8"))


print(r'\u8bf7'.encode().decode("unicode_escape"))
print('\u8bf7')


#方法2
s = r'\xe4\xbd\xa0\xe5\xa5\xbd'

def getUtf8Escape(s):
    d = []
    eval("d.append('" + s + "'.encode('raw_unicode_escape').decode('utf-8'))")
    return d[0]

print(getUtf8Escape(s))






