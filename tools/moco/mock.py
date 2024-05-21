from http.server import SimpleHTTPRequestHandler
import json
from socketserver import TCPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        # 读取请求体数据
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length)

        # 解析请求体中的 JSON 数据
        data = json.loads(request_body)

        # 读取 字段并进行输出
        fundnum = data.get('param').get('capitalAccount')
        
        print("===\n"+fundnum+"\n===")
        
        data=""
        if fundnum=="945001":
            # 构建要返回的 JSON 数据
            data = {
                "head": {
                    "reqNo": "20220117195150000001",
                    "reqDate": "20220117",
                    "reqTime": "195250",
                    "reqSys": "ZY"
                },
                "param": {
                    "rtnCode": "000000",
                    "rtnMsg": "成功",
                    "rtnRsn": "",
                    "data": "9999"
                }
            }
        else:
            # 构建要返回的 JSON 数据
            data = {
                "head": {
                    "reqNo": "20220117195150000001",
                    "reqDate": "20220117",
                    "reqTime": "195250",
                    "reqSys": "ZY"
                },
                "param": {
                    "rtnCode": "111111",
                    "rtnMsg": "失败",
                    "rtnRsn": "",
                    "data": "7777"
                }
            }
        
        # 设置响应头为 JSON 类型
        self.send_response(200)
        self.send_header('Content-type', 'application/json;charset=UTF-8')
        self.send_header("Access-Control-Allow-Origin", '*')
        self.end_headers()

        print(data)

        # 将数据转换为 JSON 字符串
        json_data = json.dumps(data,ensure_ascii=False)

        # 发送响应内容
        self.wfile.write(json_data.encode())

if __name__ == '__main__':
    port=9090
    server_address = ('localhost', port)
    httpd = TCPServer(server_address, MyHandler)
    print('Starting server at http://localhost:'+str(port))
    httpd.serve_forever()