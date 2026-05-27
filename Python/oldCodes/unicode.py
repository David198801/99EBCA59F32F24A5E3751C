#-*-coding:utf-8-*-
#--coding:utf-8--
#coding:utf-8

a = '\u3010\u7bb1\u5ead\u8033\u304b\u304d\u3011\u5b89\u7720\u5e97 \u9053\u8349\u5c4b  \u306f\u3053\u3079\u3089\u3010\u8033\u8210\u3081\u3011'
b = u'\u3010\u7bb1\u5ead\u8033\u304b\u304d\u3011\u5b89\u7720\u5e97 \u9053\u8349\u5c4b  \u306f\u3053\u3079\u3089\u3010\u8033\u8210\u3081\u3011'
print a
print b
print a.decode("unicode_escape")

c = "\\xe4\\xb8\\xad"
print c.decode("string_escape")
print b"\xcf\xb5\xcd\xb3\xd5\xd2\xb2\xbb\xb5\xbd\xd6\xb8\xb6\xa8\xb5\xc4\xce\xc4\xbc\xfe\xa1\xa3".decode("gbk")
e = r"\xcf\xb5\xcd\xb3\xd5\xd2\xb2\xbb\xb5\xbd\xd6\xb8\xb6\xa8\xb5\xc4\xce\xc4\xbc\xfe\xa1\xa3"
exec '''f = "{0}"'''.format(e)
print f.decode("gbk")

d = 'G:/\xd2\xf4\xc9\xf9/\xd0\xc2\xbd\xa8\xce\xc4\xbc\xfe\xbc\xd0/RJ206132-\xd7\xb5\xb2\xcb\xa4\xc8\xa4\xa4\xa4\xc3\xa4\xd1\xa4\xa4\xcf\xc4\xd0\xdd\xa4\xdf?\xa1\xab\xb8\xca\xa4\xaf\xa4\xc6\xa5\xc8\xa5\xed\xa5\xc8\xa5\xed\xa4\xca\xa1\xa2\xb7N\xb8\xb6\xa4\xb1\xa4\xa8\xa4\xc3\xa4\xc1\xa1\xab\xc1\xa2\xcc\xe5\xd2\xf4\xc9\xf9\xb8\xb6\xa4\xad.rar'
print d.decode("gbk")

print u'G:/\u97f3\u58f0/\u65b0\u5efa\u6587\u4ef6\u5939/RJ206132 \u690e\u83dc\u3068\u3044\u3063\u3071\u3044\u590f\u4f11\u307f??\u7518\u304f\u3066\u30c8\u30ed\u30c8\u30ed\u306a\u3001\u7a2e\u4ed8\u3051\u3048\u3063\u3061?\u7acb\u4f53\u97f3\u58f0\u4ed8\u304d'



