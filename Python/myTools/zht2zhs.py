#coding:utf-8
import zhconv

fileName="output.txt"
with open(fileName,"r",encoding="utf8") as txt:
    r = txt.read()
    text = zhconv.convert(r, 'zh-hans')
    with open(fileName+"_zhs.txt","w",encoding="utf8") as otxt:
        otxt.write(text)