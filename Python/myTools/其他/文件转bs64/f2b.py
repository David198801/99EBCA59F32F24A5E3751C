#coding:UTF-8
import base64
f=open(r'./f/附件2.pdf','rb')
b=open(r'./b/附件2.pdf.txt','wb')
b64=base64.b64encode(f.read())
b.write(b64)
b.close()
f.close()
