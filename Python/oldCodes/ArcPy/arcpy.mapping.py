#coding:utf-8
import arcpy
from arcpy import env
from arcpy.sa import *
env.workspace = r"C:\Users\admin\Documents\ArcGIS\数据\河南及周边地级市"
for i in range(12):
    m=str(i+1)
    outKrig = Kriging("city3.shp",m, KrigingModelOrdinary("SPHERICAL"), 2.4853777359838E-3)
    outKrig.save(r"D:\ArcGIS\Default.gdb\HenanAroud_kriging_"+m)

for i in range(12):
    m=str(i+1)
    arcpy.Clip_management(
        r"D:\ArcGIS\Default.gdb\HenanAroud_kriging_"+m, "#",
        r"D:\ArcGIS\Default.gdb\Henan_kriging_"+m, r"C:\Users\admin\Documents\ArcGIS\数据\河南及周边地级市\地级市行政范围.shp","#",True)





arcpy.env.workspace=r"D:\ArcGIS\Default.gdb"
mxd = arcpy.mapping.MapDocument(r"D:\ArcGIS\sample.mxd")

df = arcpy.mapping.ListDataFrames(mxd)[0]
lyr=arcpy.mapping.ListLayers(mxd, None, df)
for i in range(12):
    mon = str(i+1)
    lyr[2].replaceDataSource(r"D:\ArcGIS\Default.gdb", "FILEGDB_WORKSPACE", "Henan_kriging_"+ mon, True)
    elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
    for j in elm:
        if j.text[:4]==u'2015':
            j.text = u'2015年{}月'.format(mon)
    mxd.saveACopy(r"D:\ArcGIS\Henan2015_{}.mxd".format(mon))
    arcpy.mapping.ExportToJPEG(mxd, r"D:\ArcGIS\Henan2015_{}.jpg".format(mon), "PAGE_LAYOUT", resolution=400)