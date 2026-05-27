import socket #导入socket库
from time import ctime
import json
import time
HOST = ''
PORT = 10194
ADDR = (HOST, PORT)
BUFFSIZE = 1024 #定义一次从socket缓冲区最多读入1024个字节
MAX_LISTEN = 5 #表示最多能接受的等待连接的客户端的个数

char_code = 'gbk'



def tcpServer():# TCP服务
    # with socket.socket() as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#AF_INET表示socket网络层使用IP协议，SOCK_STREAM表示socket传输层使用tcp协议
        # 绑定服务器地址和端口
        s.bind(ADDR)
        # 启动服务监听
        s.listen(MAX_LISTEN)
        print('等待用户接入……')
        while True:
            # 等待客户端连接请求,获取connSock
            conn, addr = s.accept()
            print('警告，远端客户:{} 接入系统！！！'.format(addr))
            # with conn:
            print('接收请求信息……')
            # 接收请求信息
            data = conn.recv(BUFFSIZE) #读取的数据一定是bytes类型，需要解码成字符串类型
            info = data.decode(char_code)
            # print('data=%s' % data)
            print(f'接收数据：{info}')

            # 响应
            resp = ''
            with open ('server.txt',encoding='UTF-8') as txt:
                resp = txt.read()
            conn.send(resp.encode(char_code))
            print('响应:'+resp)
            conn.shutdown(socket.SHUT_WR)
        s.close()
 
if __name__ == '__main__':
 
    tcpServer()