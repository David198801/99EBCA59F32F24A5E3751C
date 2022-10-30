import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
data = "MOD09A1"

index = "lswi"

inPath = "D:/paddy/" + data + "/" + year + "/bandClip/"
outPath = "D:/paddy/" + year + "/" + index + "/"

checkDir(outPath)

list_dir = os.listdir(inPath)

for res in list_dir:
    if res[-3:].isdigit() and res[:2] == "b2":
        raster_b2 = Raster(inPath + res)
        raster_b6 = Raster(inPath + res.replace("b2","b6"))
        output_raster = Float(raster_b2 - raster_b6)/Float(raster_b2 + raster_b6)
        savePath = outPath + "lswi_" + res[3:]
        output_raster.save(savePath)
        print savePath