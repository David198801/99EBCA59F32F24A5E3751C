import os
import arcpy


# path = 'D:/air/avg_shp/'
# path = 'D:/air/year_avg_shp/'
# savePath = 'D:/air/ZSJ_yavg_shp/'
path = 'D:/air/mon_avg_shp/'
savePath = 'D:/air/ZSJ_mavg_shp/'

list_dir = os.listdir(path)

# clip_features = r"D:\ArcGIS\ZSJ_around.shp"
clip_features = r"D:\ArcGIS\Export_Output.shp"
for shp in list_dir:
    if shp[-6:] == '_1.shp':
        print shp
        arcpy.Clip_analysis(path + shp, clip_features,savePath + 'ZSJ_'+shp.replace("_1",""))