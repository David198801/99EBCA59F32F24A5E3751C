# coding:utf-8
import os
import arcpy
from arcpy.sa import *

# path = "D:\\air\ZSJ_avg_shp\\"
# path = "D:\\air\ZSJ_yavg_shp\\"
path = "D:\\air\ZSJ_mavg_shp\\"

arcpy.env.workspace = r'D:\air\zKrg'
# arcpy.env.extent = r"D:\ArcGIS\ZSJ_around"
list_dir = os.listdir(path)

clip_features = ur"D:\ArcGIS\GuangZhou\区级行政区_2000.shp"
datas = {'AQI':'AQI','PM2_5':'P25','O3':'O3', 'PM10':'P10', 'SO2':'SO2', 'NO2':'NO2', 'CO':'CO'}
'''
for data in datas:
    for shp in list_dir:
        if shp[-3:] == 'shp':

            outName = 'ZKC' + shp[-10:-4] + datas[data]
            outKrig = Kriging(path + shp, data, KrigingModelOrdinary("SPHERICAL"))
            # outKrig.save('zKrg' + shp[-12:-4])
            # outKrig.save(outName)
            arcpy.Clip_management(outKrig, "#", outName, clip_features, "#", True)
            print outName
'''
for shp in list_dir:
    if shp[-3:] == 'shp':
        print shp
        outName = 'GKC' + shp[-8:-4] + 'P25'
        outKrig = Kriging(path + shp, 'PM2_5', KrigingModelOrdinary("SPHERICAL"),300)
        arcpy.Clip_management(outKrig, "#", outName, clip_features, "#", True)
        print outName

'''输出文件夹/文件名称复杂（或使用GDB)会报错，故使用简单文件夹/文件名'''
'''第一个参数in_raster为绝对路径可能报错，out_raster可以为绝对路径'''
