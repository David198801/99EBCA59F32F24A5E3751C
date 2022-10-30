# coding:utf-8
import os
import xlrd
import shapefile

# path = 'D:/air/avg/'
path = 'D:/air/mon_avg_xls/'
# path = 'D:/air/year_avg_xls/'

list_dir = os.listdir(path)

book_stations = xlrd.open_workbook('D:/air/stations/stations.xls')
sheet_stations = book_stations.sheet_by_name("Sheet1")
area = sheet_stations.col_values(0, start_rowx=0, end_rowx=None)
stationName = sheet_stations.col_values(1, start_rowx=0, end_rowx=None)
latitude = sheet_stations.col_values(2, start_rowx=0, end_rowx=None)
longitude = sheet_stations.col_values(3, start_rowx=0, end_rowx=None)

for xls in list_dir:
    book = xlrd.open_workbook(path + xls)
    sheet = book.sheet_by_name("sheet")

    shp = shapefile.Writer(shapeType=1)
    shp.field('city', 'C', '10')
    shp.field('station', 'C', '30')
    shp.field('latitude', 'N', decimal=6)
    shp.field('longitude', 'N', decimal=6)
    shp.field('AQI', 'N', decimal=2)
    shp.field('PM2_5', 'N', decimal=2)
    shp.field('O3', 'N', decimal=2)
    shp.field('PM10', 'N', decimal=2)
    shp.field('SO2', 'N', decimal=2)
    shp.field('NO2', 'N', decimal=2)
    shp.field('CO', 'N', decimal=2)

    for row_num in range(1, sheet.nrows):
        if row_num <= 100:
            start = 0
            end = 199
        elif row_num > 1394:
            end = 1494
            start = 1294
        else:
            start = row_num - 101
            end = row_num + 99
        # if row_num <= 150:
        #     start = 0
        #     end = 299
        # elif row_num > 1344:
        #     end = 1494
        #     start = 1194
        # else:
        #     start = row_num - 151
        #     end = row_num + 149

        for rowS_num in range(start, end):
            if (sheet.cell_value(row_num, 1) == stationName[rowS_num] and
                     (sheet.cell_value(row_num, 0) in area[rowS_num] or
                    area[rowS_num] in sheet.cell_value(row_num, 0))):
                shp.point(longitude[rowS_num], latitude[rowS_num])
                shp.record(city=area[rowS_num].encode("utf8"),
                           latitude=latitude[rowS_num],
                           station=stationName[rowS_num].encode("utf8"),
                           longitude=longitude[rowS_num],
                           AQI=sheet.cell_value(row_num, 2),
                           PM2_5=sheet.cell_value(row_num, 3),
                           O3=sheet.cell_value(row_num, 4),
                           PM10=sheet.cell_value(row_num, 5),
                           SO2=sheet.cell_value(row_num, 6),
                           NO2=sheet.cell_value(row_num, 7),
                           CO=sheet.cell_value(row_num, 8))
                # def recd(col):
                #     if str(sheet.cell_value(row_num, col)):
                #         print(sheet.cell_value(row_num, col))
                #         return sheet.cell_value(row_num, col)
                # shp.record(city='你好',
                #            station='a',
                #            latitude=latitude[rowS_num],
                #            longitude=longitude[rowS_num],
                #            AQI=recd(2),
                #            PM2_5=recd(3),
                #            O3=recd(4),
                #            PM10=recd(5),
                #            SO2=recd(6),
                #            NO2=recd(7),
                #            CO=recd(8))

    # shp.save('D:/air/day_avg_shp/' + xls[:-4])
    shp.save('D:/air/mon_avg_shp/' + xls[:-4])
    # shp.save('D:/air/year_avg_shp/' + xls[:-4])
    print xls
