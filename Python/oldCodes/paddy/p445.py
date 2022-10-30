import arcpy
from arcpy.sa import *
from header import *

inPath = "D:/paddy/" + year + "/lgeTrans/"
outPath = "D:/paddy/" + year + "/"
arcpy.env.workspace = outPath
arcpy.env.overwriteOutput = True

name = "paddyMaybe"

fileList = os.listdir(inPath)

for i in range(len(fileList))[::-1]:
    if not fileList[i][-3:].isdigit():
        del fileList[i]

transList = range(trans[0],trans[1] + 1)
if year in correctList:
    transList = correctDays

transFileList = []
for day in transList:
    for k in fileList:
        if (year + str(day).zfill(3)) in k:
            transFileList.append(k)


ras = Raster(inPath + transFileList[0])
print transFileList[0]

for file in transFileList[1:]:
    print file
    ras = ((Raster(inPath + file) == 1) | (ras == 1))

ras.save(name)
# ras = Raster(inPath + fileList[0])
#
# for file in fileList[1:21]:
#     print inPath + file
#     ras = ((Raster(inPath + file) == 1) | (ras == 1))
#
#
# ras2 = ras
# for file in fileList[21:40]:
#     print inPath + file
#     ras2 = ((Raster(inPath + file) == 1) | (ras2 == 1))
#
#
# ras3 = ras2
# for file in fileList[40:]:
#     print inPath + file
#     ras3 = ((Raster(inPath + file) == 1) | (ras3 == 1))
# ras3.save("paddyMaybe")