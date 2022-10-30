import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True

lswiPath = "D:/paddy/" + year + "/lswi/"

outPath = "D:/paddy/" + year + "/lswiGE015/"

checkDir(outPath)

lswiList = os.listdir(lswiPath)

for lswi in lswiList:
    if lswi[-3:].isdigit():
        lswiRaster = Raster(lswiPath + lswi)
        # maskRaster = Raster(maskPath + lswi.replace("lswi", "mask"))

        output_raster = lswiRaster>=0.15
        savePath = outPath + lswi.replace("lswi","lg015")
        output_raster.save(savePath)
        print savePath