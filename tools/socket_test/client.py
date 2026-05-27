#coding:utf-8

import socket
 
from time import ctime
HOST = '127.0.0.1'
PORT = 10276
ADDR = (HOST, PORT)
BUFFSIZE = 1024

char_code = 'gbk'
 
 
with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
    # 尝试连接服务器
    s.connect(ADDR)
    print('连接服务成功！！')
    req = ''
    with open ('client.txt',encoding='UTF-8') as txt:
        req = txt.read()
    s.send(req.encode(char_code))
    s.shutdown(socket.SHUT_WR)
    print('发送成功！')

    # 接收返回数据
    outData = s.recv(BUFFSIZE)
    print(f'返回数据信息：{outData.decode(char_code)}')