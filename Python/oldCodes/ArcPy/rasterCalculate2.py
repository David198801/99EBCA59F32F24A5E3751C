import os
import arcpy
from arcpy.sa import *

year = "2017"
data = "MOD09A1"

inPath = "D:/paddy/" + year + "/gt0/"
outPath = "D:/paddy/" + year + "/gt0/"


list_dir = os.listdir(inPath)
output_raster = Raster(inPath + "LSWI_2017001.tif")
for res in list_dir:
    if res[-3:] == 'tif':
        output_raster = ((Raster(inPath + res) == 1) & (output_raster == 1))
output_raster.save(outPath + "all.tif")
