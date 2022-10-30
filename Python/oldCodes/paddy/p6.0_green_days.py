import arcpy
from arcpy.sa import *
from header import *


ndviPath = "D:/paddy/" + year + "/ndvi/"
# maskPath = "D:/paddy/MOD09A1/" + year + "/maskClip/"
arcpy.env.overwriteOutput = True
outPath = "D:/paddy/" + year + "/ndviGT07/"

checkDir(outPath)

ndviList = os.listdir(ndviPath)

for ndvi in ndviList:
    if ndvi[-3:].isdigit():
        ndviRaster = Raster(ndviPath + ndvi)
        # maskRaster = Raster(maskPath + lswi.replace("lswi", "mask"))

        output_raster = ndviRaster>0.7
        savePath = outPath + ndvi.replace("ndvi","ng07")
        output_raster.save(savePath)
        print savePath