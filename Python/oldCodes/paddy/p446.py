import arcpy
from arcpy.sa import *
from header import *
arcpy.env.overwriteOutput = True
inPath = "D:/paddy/" + year + "/"

paddyMayRaster = arcpy.Raster(inPath + "paddymaybe")
greenRaster = arcpy.Raster(inPath + "green")
waterRaster = arcpy.Raster(inPath + "water")
greenRaster2 = arcpy.Raster(inPath + "green2")


slopeRaster = arcpy.Raster("D:/paddy/3 DEM2018/less6_reclass")

paddyRaster = (paddyMayRaster == 1) & (greenRaster == 0) & (waterRaster == 0) & (slopeRaster == 1) & (greenRaster2 == 0)

paddyReclass = Reclassify(in_raster=paddyRaster,
                          reclass_field="Value",
                          remap=RemapValue([[1,1]]),
                          missing_values="NODATA")
# transRaster.save(inPath + "test3")
save = inPath + "paddy" + year + ".shp"
arcpy.RasterToPolygon_conversion(in_raster=paddyReclass,
                                 out_polygon_features = save,
                                 simplify="NO_SIMPLIFY")
save2 = inPath + "paddy" + year + "_area" + ".shp"
arcpy.CalculateAreas_stats(save, save2)
