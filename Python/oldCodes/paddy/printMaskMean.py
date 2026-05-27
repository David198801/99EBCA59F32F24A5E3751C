#coding:utf8
import arcpy
from arcpy.sa import *
from header import *

maskPath = "D:/paddy/" + year + "/mask/"
# arcpy.env.workspace = maskPath
# 描述数据必须设置workspace
maskList = os.listdir(maskPath)
a=0
for mask in maskList:
    if mask[-3:].isdigit():
        maskRaster = Raster(maskPath+mask)
        # m = arcpy.Describe(maskPath+mask)
        m = maskRaster.mean
        print mask,m
        if m < 0.3:
            a+=1
print a
