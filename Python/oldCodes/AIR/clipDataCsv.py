#coding:utf-8
import csv
import xlwt
import time
import os

workPath = "D:/air/2017/"

def timeTrans(timeStr):
    tempTime = time.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
    resTime = time.strftime('%Y%m%d', tempTime)
    return resTime

def timeTrans2(timeStr):
    tempTime = time.strptime(timeStr,'%Y-%m-%d %H:%M:%S')
    resTime = time.strftime('%Y-%m-%d %H:%M', tempTime)
    return resTime


def writeXLS(file):
    lineNums = 0
    with open(workPath + file) as csvFile:
        for line in csvFile:
            lineNums += 1

    with open(workPath + file) as csvFile:
        rows = csv.reader(csvFile)
        next(rows)

        book = xlwt.Workbook()
        sheet = book.add_sheet("sheet")
        sheet.write(0, 0, 'updatetime')
        sheet.write(0, 1, 'AreaName')
        sheet.write(0, 2, 'jczname')
        sheet.write(0, 3, 'AQI')
        sheet.write(0, 4, 'PM2_5')
        sheet.write(0, 5, 'O3')
        sheet.write(0, 6, 'PM10')
        sheet.write(0, 7, 'SO2')
        sheet.write(0, 8, 'NO2')
        sheet.write(0, 9, 'CO')

        def writeData(row, col, data):
            if col == 0:
                sheet.write(row, col, timeTrans2(data))
            elif r"\xa1\xaa" not in repr(data) and len(data) != 0 and '-' not in data:
                if col == 1 or col == 2:
                    sheet.write(row, col, data.decode('gbk'))
                else:
                    sheet.write(row, col, float(data))

        time_csv = file[0:4] + '-' + file[4:6] + '-01 00:00:00'
        # time_csv = file[0:4] + '/' + str(int(file[4:6])) + '/1  0:00'
        row_xls = 0
        for row in rows:
            row_xls += 1
            # if time_csv == row[0]:
            if rows.line_num == lineNums:
                for i in range(10):
                    writeData(row_xls, i, row[i])
                book.save(workPath + "day_xls/" + timeTrans(time_csv) + ".xls")
                print timeTrans(time_csv)
            elif timeTrans(time_csv) == timeTrans(row[0]):
                for i in range(10):
                    writeData(row_xls, i, row[i])
            else:
                row_xls = 1
                book.save(workPath+"day_xls/" + timeTrans(time_csv)  + ".xls")
                print timeTrans(time_csv)
                time_csv = row[0]
                book = xlwt.Workbook()
                sheet = book.add_sheet("sheet")
                sheet.write(0, 0, 'updatetime')
                sheet.write(0, 1, 'AreaName')
                sheet.write(0, 2, 'jczname')
                sheet.write(0, 3, 'AQI')
                sheet.write(0, 4, 'PM2_5')
                sheet.write(0, 5, 'O3')
                sheet.write(0, 6, 'PM10')
                sheet.write(0, 7, 'SO2')
                sheet.write(0, 8, 'NO2')
                sheet.write(0, 9, 'CO')
                for i in range(10):
                    writeData(row_xls, i, row[i])

list_dir = os.listdir(workPath)
for file in list_dir:
    if file[-3:] == 'csv':
        writeXLS(file)