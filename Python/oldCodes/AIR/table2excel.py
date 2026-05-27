import os
import arcpy

arcpy.env.workspace = r'D:\air\ZSJ_mavg_shp'
path = 'D:/air/ZSJ_mavg_shp/'

list_dir = os.listdir(path)
for shp in list_dir:
    if shp[-3:] == 'shp':
        print shp
        arcpy.TableToExcel_conversion(shp, shp[:-4]+".xls")