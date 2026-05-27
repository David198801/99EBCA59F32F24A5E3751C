#coding:utf8
import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
maskPath = "D:/paddy/" + year + "/mask/"
maskList = os.listdir(maskPath)

maskLT03 = []
for mask in maskList:
    if mask[-3:].isdigit():
        maskRaster = Raster(maskPath+mask)
        # m = arcpy.Describe(maskPath+mask)
        m = maskRaster.mean
        if m < 0.3:
            maskLT03.append(mask[-3:])

print maskLT03
print len(maskLT03)

inPath = "D:/paddy/" + year + "/ndviGT07/"
outPath = "D:/paddy/" + year + "/"

name = "green"

arcpy.env.workspace = outPath

fileList = os.listdir(inPath)


for i in range(len(fileList))[::-1]:
    if (not fileList[i][-3:].isdigit()) or (fileList[i][-3:] not in maskLT03):
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
for file in fileList[25:]:
    print inPath + file
    ras3 += Raster(inPath + file)

# ras4 = ras3
# for file in fileList[35:40]:
#     print inPath + file
#     ras4 += Raster(inPath + file)
#
# ras5 = ras4
# for file in fileList[40:]:
#     print inPath + file
#     ras5 += Raster(inPath + file)
number = int(20.0/46.0*len(maskLT03))
print number
ras6 = ras3>=number

ras6.save(name)


