# coding:utf-8
import xlrd
import xlwt
import os

workPath = "D:/air/mon_avg_xls/"




wbook = xlwt.Workbook()
wsheet = wbook.add_sheet("sheet")
wsheet.write(0, 0, 'AreaName')
wsheet.write(0, 1, 'City')
wsheet.write(0, 2, 'AQI')
wsheet.write(0, 3, 'PM2_5')
wsheet.write(0, 4, 'O3')
wsheet.write(0, 5, 'PM10')
wsheet.write(0, 6, 'SO2')
wsheet.write(0, 7, 'NO2')
wsheet.write(0, 8, 'CO')

w_row = 1

list_dir = os.listdir(workPath)

for file in list_dir:
    book = xlrd.open_workbook(workPath + file)
    sheet = book.sheet_by_name("sheet")
    for row in range(1, sheet.nrows):
        for col in range(0, sheet.ncols):
            print file, w_row
            print sheet.cell_value(row, col)
            wsheet.write(w_row, col, sheet.cell_value(row, col))
        w_row += 1


wbook.save("D:/air/year_xls/" + "year_xls_2016.xls")