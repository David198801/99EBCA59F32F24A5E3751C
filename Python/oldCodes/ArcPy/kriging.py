#-*-coding:utf-8-*-
import arcpy
from arcpy.sa import *
arcpy.env.workspace=r"D:/kentucky/"
shpFile= r"corn2012_vector_pcs.shp"
outKrig = Kriging(shpFile, "OZONE", KrigingModelOrdinary("CIRCULAR", 2000, 2.6, 542, 0), 2000, RadiusFixed(20000, 1))
outKrig.save("krigout")
