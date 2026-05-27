import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
bandPath = "D:/paddy/MOD09A1/" + year + "/bandClip/"
maskPath = "D:/paddy/MOD09A1/" + year + "/maskClip/"

outPath = "D:/paddy/" + year + "/mask/"

checkDir(outPath)

maskList = os.listdir(maskPath)

for mask in maskList:
    if mask[-3:].isdigit():
        maskRaster = Raster(maskPath + mask)
        bandRaster = Raster(bandPath + mask.replace("mask","b3") + ".tif")

        output_raster = (maskRaster != 0)|(bandRaster>2000)
        savePath = outPath + mask.replace("mask","maskb")
        output_raster.save(savePath)
        print savePath