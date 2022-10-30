# coding:utf-8
import arcpy
from arcpy.sa import *
arcpy.env.workspace = r"D:\ArcGIS\nation3\kriging"
path = "D:\\ArcGIS\\nation3\\"

month = [u'一月',u'二月',u'三月',u'四月',u'五月',u'六月',u'七月',u'八月',u'九月',u'十月',u'十一月',u'十二月']
file = ["C_1999_1.shp","C_1998_1.shp"]


for f in file:
    for indexM in range(len(month)):
        outKrig = Kriging(path + f, month[indexM], KrigingModelOrdinary("SPHERICAL"),16313/16)
        outName = "kriging" + f[2:6] + str(indexM+1).zfill(2)
        outKrig.save(outName)
        print outName