# coding:utf-8
import xlrd
import xlwt
import os

workPath = "D:/air/year_xls/"

year = '2016'


def zeroNotDiv(a,b):
    if not b == 0:
        return a / b

list_dir = os.listdir(workPath)

in_file = workPath + "year_xls_2016.xls"
book = xlrd.open_workbook(in_file)
sheet = book.sheet_by_name("sheet")
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

station = sheet.cell_value(1, 1)
data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
count_data = [0, 0, 0, 0, 0, 0, 0]
count_row = 0


def accumulate(data, row_num, col_num):
    if isinstance(sheet.cell_value(row_num, col_num + 2), float):
        data[col_num] += sheet.cell_value(row_num, col_num + 2)
        count_data[col_num] += 1


for row_num in range(1, sheet.nrows):
    if sheet.cell_value(row_num, 1) == station:
        for col_num in range(7):
            accumulate(data, row_num, col_num)
    else:
        avg_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(7):
            avg_data[i] = zeroNotDiv(data[i], count_data[i])

        for i in range(7):
            if isinstance(sheet.cell_value(row_num, i + 2), float):
                data[i] = sheet.cell_value(row_num, i + 2)
            else:
                data[i] = 0.0

        count_row += 1

        for i in range(7):
            if avg_data[i] != 0:
                wsheet.write(count_row, i + 2, avg_data[i])
        wsheet.write(count_row, 1, station)
        wsheet.write(count_row, 0, sheet.cell_value(row_num - 1, 0))

        station = sheet.cell_value(row_num, 1)
        count_data = [1, 1, 1, 1, 1, 1, 1]

wbook.save("D:/air/year_avg_xls/" + "year_avg_2016.xls")
