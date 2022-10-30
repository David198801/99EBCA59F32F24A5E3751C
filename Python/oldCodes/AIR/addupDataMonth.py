# coding:utf-8
import xlrd
import xlwt
import os

workPath = "D:/air/avg/"

year = '2017'
Month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
list_dir = os.listdir(workPath)
for indexM in Month:
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
    for file in list_dir:
        if year + indexM == file[8:14]:
            book = xlrd.open_workbook(workPath + file)
            sheet = book.sheet_by_name("sheet")
            for row in range(1, sheet.nrows):
                for col in range(0, sheet.ncols):
                    wsheet.write(w_row, col, sheet.cell_value(row, col))
                w_row += 1
    saveName = "mon_xls_" + year + indexM + ".xls"
    wbook.save("D:/air/mon_xls/" + saveName)
    print saveName