import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
lswiPath = "D:/paddy/" + year + "/lswi/"
eviPath = "D:/paddy/" + year + "/evi/"
maskPath = "D:/paddy/" + year + "/mask/"
# maskPath = "D:/paddy/MOD09A1/" + year + "/maskClip/"

outPath = "D:/paddy/" + year + "/lswiGTevi/"

checkDir(outPath)

lswiList = os.listdir(lswiPath)

for lswi in lswiList:
    if lswi[-3:].isdigit() and int(lswi[-3:]) in correctDays:
        lswiRaster = Raster(lswiPath + lswi)
        eviRaster = Raster(eviPath + lswi.replace("lswi","evi"))
        maskRaster = Raster(maskPath + lswi.replace("lswi", "maskB"))
        output_raster = ((lswiRaster+0.05)>=eviRaster) & (maskRaster == 0)
        # maskRaster = Raster(maskPath + lswi.replace("lswi", "mask"))
        # output_raster = ((lswiRaster + 0.05) >= eviRaster) & (maskRaster == 0)
        savePath = outPath + lswi.replace("lswi","lge")
        output_raster.save(savePath)
        print savePath