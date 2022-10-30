#coding:utf-8
import os
import xlrd
import xlwt

inPath = 'D:/air/day_xls/'
savePath = 'D:/air/avg/'

year='2017'
Month = ['01', '02',  '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
Days = ['01', '02',  '03', '04', '05', '06', '07', '08', '09', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

def zeroNotDiv(a,b):
    if not b == 0:
        return a / b

for indexM in Month:
    for indexD in Days:
        in_file = inPath + year + indexM + indexD + ".xls"
        if os.path.exists(in_file):
            book = xlrd.open_workbook(in_file)
            sheet = book.sheet_by_name("sheet")
            wbook = xlwt.Workbook()
            wsheet = wbook.add_sheet("sheet")
            wsheet.write(0, 0, 'Area')
            wsheet.write(0, 1, 'Station')
            wsheet.write(0, 2, 'AQI')
            wsheet.write(0, 3, 'PM2_5')
            wsheet.write(0, 4, 'O3')
            wsheet.write(0, 5, 'PM10')
            wsheet.write(0, 6, 'SO2')
            wsheet.write(0, 7, 'NO2')
            wsheet.write(0, 8, 'CO')

            station = sheet.cell_value(1,2)
            data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            count_data = [0, 0, 0, 0, 0, 0, 0]
            count_row = 0

            def accumulate(data,row_num,col_num):
                if isinstance(sheet.cell_value(row_num, col_num + 3),float):
                    data[col_num] += sheet.cell_value(row_num, col_num + 3)
                    count_data[col_num] += 1

            for row_num in range(1,sheet.nrows):
                if sheet.cell_value(row_num, 2) == station:
                    for col_num in range(7):
                        accumulate(data, row_num, col_num)
                else:
                    avg_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    for i in range(7):
                        avg_data[i] = zeroNotDiv(data[i],count_data[i])


                    for i in range(7):
                        if isinstance(sheet.cell_value(row_num, i + 3), float):
                            data[i] = sheet.cell_value(row_num, i+3)
                        else:
                            data[i] = 0.0

                    count_row += 1

                    for i in range(7):
                        if avg_data[i] != 0:
                            wsheet.write(count_row, i + 2, avg_data[i])
                    wsheet.write(count_row, 1, station)
                    wsheet.write(count_row, 0, sheet.cell_value(row_num-1, 1))

                    station = sheet.cell_value(row_num, 2)
                    count_data = [1, 1, 1, 1, 1, 1, 1]
            saveName = 'Day_avg_' +year + indexM + indexD + ".xls"
            wbook.save(savePath  + saveName)
            print saveName