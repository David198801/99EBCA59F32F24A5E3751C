import os
import arcpy

# arcpy.env.workspace = "D:/air/avg_shp"
# path = 'D:/air/avg_shp/'
# arcpy.env.workspace = 'D:/air/mon_avg_shp/'
# path = 'D:/air/mon_avg_shp/'
# arcpy.env.workspace = 'D:/air/year_avg_shp/'
# path = 'D:/air/year_avg_shp/'
arcpy.env.workspace = 'D:/air/day_shp/'
path = 'D:/air/day_shp/'

list_dir = os.listdir(path)
spatial_ref = arcpy.SpatialReference("Beijing 1954")
# dataset = "D:/air/shp/poly_of_wuhan.shp"
# spatial_ref = arcpy.Describe(dataset).spatialReference
for shp in list_dir:
    if shp[-3:] == 'shp':
        arcpy.DefineProjection_management(shp, spatial_ref)