#coding:utf-8
import os
import arcpy
from arcpy.sa import *

path = "D:\\air\\zKrg\\"

mxd = arcpy.mapping.MapDocument(r"D:\air\sample.mxd")

df = arcpy.mapping.ListDataFrames(mxd)[0]
lyr=arcpy.mapping.ListLayers(mxd, None, df)

year = '17'

# year = '2016'
Month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
Days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

# for indexM in Month:
#     for indexD in Days:
#         fileName = 'zkc' + year + indexM + indexD + 'p25'
#         if os.path.exists(path+fileName):
#             lyr[2].replaceDataSource(r"D:\air\zKrg", "RASTER_WORKSPACE", fileName, True)
#             elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
#             for j in elm:
#                 if u'2016' in j.text:
#                     j.text = u'2016年{0}月{1}日'.format(indexM, indexD)
#                     print j.text
#             mxd.saveACopy("D:\\air\\mxd\\" + fileName + ".mxd")
#             arcpy.mapping.ExportToJPEG(mxd, "D:\\air\\picture\\" + fileName + ".jpg", "PAGE_LAYOUT", resolution=400)

for indexM in Month:
    fileName = 'gkc' + year + indexM + 'p25'
    if os.path.exists(path + fileName):
        lyr[2].replaceDataSource(r"D:\air\zKrg", "RASTER_WORKSPACE", fileName, True)
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
        for j in elm:
            if u'年' in j.text:
                j.text = u'2017年{0}月'.format(indexM)
                print j.text
        mxd.saveACopy("D:\\air\\mxd\\" + fileName + ".mxd")
        arcpy.mapping.ExportToJPEG(mxd, "D:\\air\\picture\\" + fileName + ".jpg", "PAGE_LAYOUT", resolution=400)
