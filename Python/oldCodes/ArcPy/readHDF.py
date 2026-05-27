# import arcpy
#
# hdfList = arcpy.ExtractSubDataset_management(r"D:\paddy\MOD09A1\2017\MOD09A1.A2017001.h27v05.006.2017017151934.hdf",
#                                              r"D:\paddy\MOD09A1\2017\aa11111.tif", "0;1;2;3")
from osgeo import gdal

# ds = gdal.Open(r"D:\paddy\MOD09A1\2017\mask\meta.2017001.h27v05.hdf")
# gdal.Translate(r"D:\paddy\sfasdfasd.tif",ds)
ds = gdal.Open(r"D:\paddy\MOD09A1\2017\MOD09A1.A2017337.h27v05.006.2017346035200.hdf")
print ds.GetSubDatasets()[1][0]
gdal.Translate(r"D:\paddy\sfasdfasd.tif",ds.GetSubDatasets()[0][0])