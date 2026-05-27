import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
data = "MOD09A1"
index = "evi"

inPath = "D:/paddy/" + data + "/" + year + "/bandClip/"
outPath = "D:/paddy/" + year + "/" + index + "/"

checkDir(outPath)

list_dir = os.listdir(inPath)

for res in list_dir:
    if res[-3:].isdigit() and res[:2] == "b1":
        raster_b1 = Raster(inPath + res)
        raster_b2 = Raster(inPath + res.replace("b1", "b2"))
        raster_b3 = Raster(inPath + res.replace("b1", "b3"))
        output_raster = 2.5*Float(raster_b2 - raster_b1)/(Float(raster_b2) + Float(6*raster_b1) - 7.5*Float(raster_b3) + 10000.0)
        savePath = outPath + "evi_" + res[3:]
        output_raster.save(savePath)
        print savePath