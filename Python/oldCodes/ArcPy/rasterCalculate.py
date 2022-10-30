import os
import arcpy
from arcpy.sa import *

year = "2017"
data = "MOD09A1"

inPath = "D:/paddy/" + year + "/"
outPath = "D:/paddy/" + year + "/gt0/"


list_dir = os.listdir(inPath)

for res in list_dir:
    if res[-3:] == 'tif':
        output_raster = (Raster(inPath + res)>0)
        output_raster.save(outPath + res)
