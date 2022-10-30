import requests
from bs4 import BeautifulSoup

txtPath = r"D:\linshi2\新建 文本文档.txt"
outTxtPath = r"D:\linshi2\out.txt"
outTxt = open(outTxtPath, "w", encoding="utf-8-sig")
urlList = []
with open(txtPath, "r") as txt:
    urlList = txt.readlines()

urlPart = r"http://www.wznk120.com"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
    "Cache-Control": "max-age=0",
    "Host": "www.wznk120.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http//www.wznk120.com/book/2214/463237.html",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

for url in urlList:
    fullUrl = urlPart + url.replace("\r","").replace("\n","")
    print(fullUrl)
    r = requests.get(fullUrl, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    chapterDivList = soup.find_all(name="div", class_="con_show_l")
    pList = chapterDivList[0].select("div.con_show_l>p")
    print(pList)
    title = pList[0].string
    outTxt.write(title + "\n\n")
    for p in pList[1:]:
        outTxt.write("    " + p.string + "\n\n")
    outTxt.write("\n\n")
outTxt.close()
