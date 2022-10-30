import arcpy
from header import *

inPath = "D:/paddy/2017/evi/"


list_dir = os.listdir(inPath)

trans = [113,129+40]
transList = range(trans[0],trans[1]+1)

for res in list_dir:
    if res[-3:].isdigit():
        for i in transList:
            if str(i) in res:
                ras = arcpy.Raster(inPath + res)
                print res, ras.mean

