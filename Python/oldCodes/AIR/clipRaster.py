import os
import arcpy

path = "D:\\air\\HuBei"
clip_features = r"D:\air\shp\poly_of_wuhan.shp"
for i in range(3,4):
    tPath = path + str(i)
    arcpy.env.workspace = tPath
    fileList = os.listdir(tPath)
    for file in fileList:
        if file[-3:] != "xml" and file != "info":
            arcpy.Clip_management(file, "#", "D:\\air\\WuHan\\" + file + ".tif", clip_features, "#", True)
            print file
