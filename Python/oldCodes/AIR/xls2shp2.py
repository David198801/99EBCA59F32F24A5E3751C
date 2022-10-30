# coding:utf-8
import os
import xlrd
import shapefile

path = 'D:/air/day_xls/'
list_dir = os.listdir(path)

savePath = 'D:/air/day_shp/'

for xls in list_dir:
    book = xlrd.open_workbook(path + xls)
    sheet = book.sheet_by_name("sheet")

    shp = shapefile.Writer(shapeType=1)
    shp.field('latitude', 'N', decimal=6)
    shp.field('longitude', 'N', decimal=6)
    shp.field('elevation', 'N', decimal=2)
    shp.field('temp', 'N', decimal=2)

    for row_num in range(1, sheet.nrows):
        longitude = sheet.cell_value(row_num, 1)
        latitude = sheet.cell_value(row_num, 0)
        elevation = sheet.cell_value(row_num, 2)
        temperature = sheet.cell_value(row_num, 3)

        shp.point(longitude, latitude)
        shp.record(latitude=latitude,
                   longitude=longitude,
                   elevation=elevation,
                   temp=temperature)

    saveName = xls[:-4] + ".shp"
    shp.save(savePath+saveName)
    print saveName