import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
inPath = "D:/paddy/" + year + "/ndviGT07/"
outPath = "D:/paddy/" + year + "/"

name = "green"

arcpy.env.workspace = outPath

fileList = os.listdir(inPath)

for i in range(len(fileList))[::-1]:
    if not fileList[i][-3:].isdigit():
        del fileList[i]



ras = Raster(inPath + fileList[0])

for file in fileList[1:15]:
    print inPath + file
    ras += Raster(inPath + file)
# ras.save()


ras2 = ras
for file in fileList[15:25]:
    print inPath + file
    ras2 += Raster(inPath + file)

ras3 = ras2
for file in fileList[25:35]:
    print inPath + file
    ras3 += Raster(inPath + file)

ras4 = ras3
for file in fileList[35:40]:
    print inPath + file
    ras4 += Raster(inPath + file)

ras5 = ras4
for file in fileList[40:]:
    print inPath + file
    ras5 += Raster(inPath + file)

ras6 = ras5>=20

ras6.save(name)
