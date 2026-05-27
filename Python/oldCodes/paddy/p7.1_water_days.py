import os
import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
ndviPath = "D:/paddy/" + year + "/ndvi/"
lswiPath = "D:/paddy/" + year + "/lswi/"

outPath = "D:/paddy/" + year + "/ndviLT01andLTlswi/"

checkDir(outPath)

ndviList = os.listdir(ndviPath)

for ndvi in ndviList:
    if ndvi[-3:].isdigit():
        ndviRaster = Raster(ndviPath + ndvi)
        lswiRaser = Raster(lswiPath + ndvi.replace("ndvi","lswi"))
        output_raster = (ndviRaster<0.1)&(ndviRaster<lswiRaser)
        savePath = outPath + ndvi.replace("ndvi","nl01l")
        output_raster.save(savePath)
        print savePath