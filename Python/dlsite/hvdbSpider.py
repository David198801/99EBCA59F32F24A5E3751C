import requests
from bs4 import BeautifulSoup
import re
import time
import xlwt

name = "猫乃緒みみ"
name = "小春日より"

url = "http://hvdb.me/Dashboard/CVWorks/" + name
outPath = r"E:/音声/list/"
outPath = r"D:/linshi/"
rjTxtPath = outPath + name + "_hvdb.txt"
excelPath = outPath + name + "_hvdb.xls"

url = "http://hvdb.me/Dashboard/AllWorks/"
rjTxtPath = outPath + "all" + "_hvdb.txt"
excelPath = outPath + "all" + "_hvdb.xls"

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Cache-Control":"max-age=0",
"Cookie":"__cfduid=d2f42942eede451ddb79682e0e95e94a31582361889; __RequestVerificationToken=jaz3maSloNC3DBSlTW4ye__NJmB21BIpdGB92gYqO1cN7AkdMH_1OlvW0vLgjxO_Il1YfHzAx5_JApzkO3uXAOpw_-R_Q0D0JW1deqQUK5o1",
"Host":"hvdb.me",
"Proxy-Connection":"keep-alive",
"Referer":"http//hvdb.me/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

allList = []
pageNum = 0
workNum = [0]

def table2list(table,allList):
    rowLabelList = table.find_all(name="tr")
    rowLabelList = rowLabelList[1:]

    for rowLabel in rowLabelList:
        rjLabelList = rowLabel.find_all(name="td", class_="center-parent")
        rjCode = rjLabelList[0].p.string
        rjCode = filter(lambda ch: ch in '0123456789', rjCode)
        rjCode = "".join(rjCode)
        '''
        if len(rjCode) < 6:
            for i in range(6-len(rjCode)):
                rjCode = "0" + rjCode
        '''
        rjCode = "RJ" + rjCode
        workNameLabelList = rowLabel.find_all(name="td", class_="col-md-3")
        workName = workNameLabelList[0].a.string
        productLabelList = rowLabel.find_all(name="td", class_="col-md-1")
        product = productLabelList[0].a.string.replace("\n", "")
        cvLabelList = rowLabel.find_all(name="td", class_="col-md-2")[0].find_all(name="a")
        cv = ""
        for cvLabel in cvLabelList:
            cv += cvLabel.string
            cv += ","
        cv = cv[:-1]
        rowList = [rjCode,workName,product,cv]
        allList.append(rowList)
        workNum[0] += 1


firstPage = requests.get(url,headers=headers)
soupFirst = BeautifulSoup(firstPage.text, features="lxml")
tableLabelList = soupFirst.find_all(name="table",class_="table")

table2list(tableLabelList[0],allList)
pageNum += 1
print("page",end="")
print(pageNum)


'''
paginationUL = soupFirst.find_all(name="ul",class_="pagination")
rexPage = re.compile(r".Dashboard.+")
linkLabelList = paginationUL[0].find_all(name="a",href=rexPage)
linkList = ["http://hvdb.me" + x["href"] for x in linkLabelList]
linkList = linkList[:-1]
pageAll = len(linkList)+1
'''

myp = 15
linkList = []
for nn in range(2,myp+1):
    linkn = "http://hvdb.me/Dashboard/AllWorks/?page=页数&pageSize=15".replace("页数",str(nn))
    linkList.append(linkn)

pageAll = myp

time.sleep(1)
for link in linkList:
    otherPage =requests.get(link,headers=headers)
    soupOther = BeautifulSoup(otherPage.text, features="lxml")
    tableLabelList = soupOther.find_all(name="table", class_="table")
    table2list(tableLabelList[0], allList)
    pageNum += 1
    print("page"+str(pageNum)+"/" +str(pageAll))
    time.sleep(1)
    
#allList.sort()

print("all =",workNum[0])

with open(rjTxtPath,"w") as txt:
    for row in allList:
        txt.write(row[0])
        txt.write("\n")

workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet(name)
worksheet.col(0).width = 12*256
worksheet.col(1).width = 100*256
worksheet.col(2).width = 50*256
worksheet.col(3).width = 50*256
worksheet.write(0,0,"RJ Code")
worksheet.write(0,1,"标题")
worksheet.write(0,2,"社团")
worksheet.write(0,3,"声优")
for rowNum in range(len(allList)):
    for colNum in range(len(row)):
        worksheet.write(rowNum+1, colNum, allList[rowNum][colNum])
workbook.save(excelPath)