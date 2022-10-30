import os
import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
inPath = "D:/paddy/" + year + "/lswiGE015/"
outPath = "D:/paddy/" + year + "/"

name = "green2"

arcpy.env.workspace = outPath

fileList = os.listdir(inPath)

for i in range(len(fileList))[::-1]:
    if not fileList[i][-3:].isdigit():
        del fileList[i]



ras = Raster(inPath + fileList[0])

for file in fileList[1:15]:
    print inPath + file
    ras = ((Raster(inPath + file) == 1) & (ras == 1))
# ras.save()


ras2 = ras
for file in fileList[15:25]:
    print inPath + file
    ras2 = ((Raster(inPath + file) == 1) & (ras2 == 1))

ras3 = ras2
for file in fileList[25:35]:
    print inPath + file
    ras3 = ((Raster(inPath + file) == 1) & (ras3 == 1))

ras4 = ras3
for file in fileList[35:40]:
    print inPath + file
    ras4 = ((Raster(inPath + file) == 1) & (ras4 == 1))

ras5 = ras4
for file in fileList[40:]:
    print inPath + file
    ras5 = ((Raster(inPath + file) == 1) & (ras5 == 1))

ras5.save(name)
