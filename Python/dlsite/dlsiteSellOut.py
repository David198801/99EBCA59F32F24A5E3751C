import requests
from bs4 import BeautifulSoup
import xlwt

outPath = r"E:/音声/"
mode = 1
year = 2020
if mode == 1:
    beginYear = 2020
    beginMonth = 1
    endYear = 2020
    endMonth = 1
elif mode ==2:
    beginYear = year
    endYear = year
    beginMonth = 1
    endMonth = 12

allMonthList = []
for y in range(beginYear,endYear+1):
    if y == beginYear:
        for m in range(beginMonth,13):
            allMonthList.append(str(y)+"-"+str(m).zfill(2))
    elif y == endYear:
        for m in range(1,endMonth+1):
            allMonthList.append(str(y)+"-"+str(m).zfill(2))
    else:
        for m in range(1,13):
            allMonthList.append(str(y)+"-"+str(m).zfill(2))
allMonthList = ["2020-1"]
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('販売終了作品')
worksheet.col(0).width = 12*256
worksheet.col(1).width = 20*256
worksheet.col(2).width = 10*256
worksheet.col(3).width = 200*256

worksheet.write(0,0,"日付")
worksheet.write(0,1,"サークル名")
worksheet.write(0,2,"作品ID")
worksheet.write(0,3,"作品名")

url = "https://www.dlsite.com/maniax/info/sellend/=/month/"

colNum = 0
rowNum = 1
for ms in allMonthList:
    urlM = url + ms
    while True:
        try:
            mPage = requests.get(urlM, timeout=5)
            break
        except:
            continue

    mSoup = BeautifulSoup(mPage.text, features="lxml")
    mTable = mSoup.find_all(name="table",class_="work_update_history")[0]
    mRowList = mTable.find_all(name="tr")
    for row in mRowList[1:]:
        updateDate = row.find_all(name="td",class_="update_date")[0].string
        updateDate = str(updateDate)
        rjCode = row.find_all(name="li",class_="work_no")[0].string
        voiceName = row.find_all(name="li",class_="work_name")[0].string
        publisher = row.find_all(name="td",class_="update_circle")[0].a.string

        worksheet.write(rowNum, colNum, updateDate)
        colNum += 1
        worksheet.write(rowNum, colNum, publisher)
        colNum += 1
        worksheet.write(rowNum, colNum, rjCode)
        colNum += 1
        worksheet.write(rowNum, colNum, voiceName)
        colNum += 1

        colNum = 0
        rowNum += 1

    print(ms)


fileName = "販売終了作品 " + str(beginYear) + str(beginMonth).zfill(2) + "-" + str(endYear) + str(endMonth).zfill(2)
fileName = fileName + ".xls"

workbook.save(outPath + fileName)
