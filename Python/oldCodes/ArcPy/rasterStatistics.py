import arcpy
import os

inDir = "D:/paddy/2017/"

fileList = os.listdir(inDir)

for file in fileList:
    if file[-3:] == "tif":
        inRas = arcpy.Raster(inDir + file)
        m = inRas.mean
        if m:
            print file[:-4] + " " + str(m)
        else:
            arcpy.CalculateStatistics_management(inRas)
            print m