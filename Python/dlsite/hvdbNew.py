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

url = "http://hvdb.me/Dashboard/AllWorks/?page=1&sort=datesort&pageSize=50"
rjTxtPath = outPath + "all" + "_hvdb.txt"
excelPath = outPath + "all" + "_hvdb.xls"

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Cache-Control":"max-age=0",
"Cookie":"__cfduid=de9062354df09c1cb3cba97d2856c63831601520698; __RequestVerificationToken=nC8BoxCd3Z9H0CoWiPVDw3OIPHWsmA5zRvmCWZ1pJzzWOLZcobVrFhGHJUnU57taMrgMTiov-LO_qDyHT-PoKxEbRvn65Qhzc3utNhNZxvs1; .AspNet.ApplicationCookie=vW_aqEEDY8JzRl5l0Fu3BHjwabGwrsSY55iPG7Z_VNfcyu2pioX4sa8NZ_9AFvH2yz22kh-hOyMgtrbaeUO0T2VmpnlD5bBJDUjcVHNu7XNxowER-ITzORJ4D3mgBv3fAOCU9J2n5cJuibbMX4Z6SCiYboc2q3lH1iouif23Wu1vY9wCHbhkFEJ3ms36WHhfvOXtgrd8Pll1Yn4XkM6Qx_ylYTI5OWc1lVPN7p6hu1fi8WvboFfJO074uK-1jPjL3nnUGNeqLxoOn8URPtTcnJ70BDa9xpEGuxkab90n5BfSl8N7rbmU9DAYaW9c86fjx10_M5tXnkTRa_lFEblRcbT4sFfrd8XKZG13pJsOmGpgYg8NFG65ef8qsWpImlT-UZj9-a6JNECeL2B8QbKsrJIcewEBkTUBkDCI_weowBRp1TFdHVX2NyVarfIpFdyc_Q5Wvtw0cUGcknHEHxmCwSCagbNeMJ1FP0Z2xRmiaLgRZeQ38QWYEAz0uM4fFwC45F5U9u_3VWToqJx6d9R48Q",
"Host":"hvdb.me",
"Proxy-Connection":"keep-alive",
"Referer":"hhttp://hvdb.me/Dashboard/AllWorks/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}



allList = []
workNum = [0]


def table2list(table, allList):
    rowLabelList = table.find_all(name="tr")
    rowLabelList = rowLabelList[1:]

    for rowLabel in rowLabelList:
        rjLabelList = rowLabel.find_all(name="td", class_="center-parent")
        rjCode = rjLabelList[0].p.string
        rjCode = filter(lambda ch: ch in '0123456789', rjCode)
        rjCode = "".join(rjCode)
        

        

        if len(rjCode) < 6:
            for i in range(6-len(rjCode)):
                rjCode = "0" + rjCode
        rjCode = "RJ" + rjCode

        workNameLabelList = rowLabel.find_all(name="td", class_="col-md-3")
        workName = workNameLabelList[0].a.string
        productLabelList = rowLabel.find_all(name="td", class_="col-md-1")
        product = productLabelList[0].a.string.replace("\n", "")
        while product[0] == " ":
            product = product[1:]

        cvLabelList = rowLabel.find_all(name="td", class_="col-md-2")[0].find_all(name="a")
        cv = ""
        for cvLabel in cvLabelList:
            cv += cvLabel.string
            cv += ","
        cv = cv[:-1]
        # 英文名为第2个col-md-3
        englishName = workNameLabelList[1].string

        # tag为第3个col-md-3
        tagLabelList =  workNameLabelList[2].find_all(name="a")
        tag = ""
        for tagLabel in tagLabelList:
            tag += tagLabel.string
            tag += ","
        tag = tag[:-1]

        # downloadtag为第3个center-parent
        downloadtag = rjLabelList[2].string

        rowList = [rjCode, workName, englishName, product, cv, tag, downloadtag]
        allList.append(rowList)
        workNum[0] += 1


linkList = []

myp = 427

titleSwitch = False
pageNum = 401
endNum = 427

for nn in range(pageNum, endNum + 1):

    linkn = "http://hvdb.me/Dashboard/AllWorks/?page=页数&sort=datesort&pageSize=50".replace("页数", str(nn))
    linkList.append(linkn)

pageAll = myp



for link in linkList:

    while True:
        try:
            otherPage = requests.get(link, headers=headers, timeout=10)
            break
        except Exception as e:
            print(e)
            continue
    soupOther = BeautifulSoup(otherPage.text, features="lxml")
    tableLabelList = soupOther.find_all(name="table", class_="table")
    
    table2list(tableLabelList[0], allList)
    
    print("page" + str(pageNum) + "/" + str(pageAll))
    pageNum += 1

# allList.sort()

print("all =", workNum[0])

with open(rjTxtPath, "w") as txt:
    for row in allList:
        txt.write(row[0])
        txt.write("\n")

workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet(name)
worksheet.col(0).width = 12 * 256
worksheet.col(1).width = 50 * 256
worksheet.col(2).width = 50 * 256
worksheet.col(3).width = 30 * 256
worksheet.col(4).width = 30 * 256
worksheet.col(5).width = 30 * 256
worksheet.col(6).width = 3 * 256

if titleSwitch:
    worksheet.write(0, 0, "RJ Code")
    worksheet.write(0, 1, "Title")
    worksheet.write(0, 2, "English Title")
    worksheet.write(0, 3, "Circle")
    worksheet.write(0, 4, "CV")
    worksheet.write(0, 5, "Tags")
    worksheet.write(0, 6, "Download?")
    
for rowNum in range(len(allList)):
    for colNum in range(len(row)):
        worksheet.write(rowNum + 1, colNum, allList[rowNum][colNum])
workbook.save(excelPath)