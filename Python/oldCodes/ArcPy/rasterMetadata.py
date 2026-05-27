from osgeo import gdal
import inspect
dataset = gdal.Open(r'D:/kentucky/polygonclip/CDL_2008_clip_20171008092522_678743273.tif')
img=gdal.Open(r'D:/kentucky/img3.tif',1)
pcs=dataset.GetProjection()
tsf=dataset.GetGeoTransform()
img.SetGeoTransform(tsf)
img.SetProjection(pcs)