#coding:utf-8
import requests
import base64
import re
import webbrowser
import os
urlHdf=r'https://e4ftl01.cr.usgs.gov/MOLT/MOD09A1.006/2000.02.18/MOD09A1.A2000049.h00v08.006.2015136143535.hdf'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
print u'输入结束请按回车键'
pwCheck=raw_input(u'读取默认密码，若需修改请')
if username == 'sign':
    webbrowser.open('https://urs.earthdata.nasa.gov//users/new')
try:
    pwR = open("pw.txt",'r')
    lPw=pwR.readlines()
    username=lPw[1]
    password=lPw[3]
except IOError:
    print u'下载需要帐号，若未注册请输入“sign”打开注册网站'
    username = raw_input(u'请输入用户名：')
    password = raw_input(u'请输入密码：')
    fp = open("pw.txt", 'w')
    fp.write(u'用户名：\n'.encode('utf-8'))
    fp.write(username+'\n')
    fp.write(u'密码：\n'.encode('utf-8'))
    fp.write(password)
    fp.close()
    print u'帐号密码已储存到程序所在目录“pw.txt”，下次启动默认读取'
print username,password
a=raw_input('aaa')
pwB64=base64.b64encode(username+':'+password)
headersPw=headers
headersPw['Authorization']='Basic '+pwB64
rpUrlHdf=requests.get(urlHdf,headers=headers,allow_redirects=False)
rpLogin=requests.get(rpUrlHdf.headers['Location'],headers=headersPw,allow_redirects=False)
rpCookie=requests.get(rpLogin.headers['Location'],headers=headers,allow_redirects=False)
cookieData=re.match(r'(DATA=.+);.+',rpCookie.headers['Set-Cookie']).group(1)