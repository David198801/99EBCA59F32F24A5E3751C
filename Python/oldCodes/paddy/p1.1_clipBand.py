#coding:utf8
import arcpy
from header import *
arcpy.env.overwriteOutput = True
data = "MOD09A1"

DataType = "band"
# DataType = "mask"

inPath = "D:/paddy/" + data + "/" + year + "/" + DataType +"Tif/"
outPath = "D:/paddy/" + data + "/" + year + "/" + DataType + "Clip/"

checkDir(outPath)

fileList = os.listdir(inPath)

clip_features = "D:/paddy/hubei_Project.shp"

for file in fileList:
    if file[-3:] == "tif":
        arcpy.Clip_management(in_raster=inPath + file, out_raster=outPath + file[:-4],
                              # rectangle="10184572.8344024 702601.635045277 12652217.423091 3700136.41414965",
                              in_template_dataset=clip_features, clipping_geometry="ClippingGeometry")
        print file