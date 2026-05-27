#-*-coding:utf-8-*-
from PIL import Image
from osgeo import gdal
filePath=r'D:/kentucky/polygonclip/CDL_2012_clip_20171008092522_678743273.tif'
newFilePath=r"D:/kentucky/Corn2012_clean.tif"
imgPath=Image.open(filePath)
imgRGB=imgPath.convert('RGB')
rgbValue=[255,211,0]
img= imgRGB.load()
def checkPixRGB(imgPix,coordinate,rgbList):
    if (imgPix[coordinate[0],coordinate[1]][0]==rgbList[0] and
        imgPix[coordinate[0],coordinate[1]][1]==rgbList[1] and
        imgPix[coordinate[0],coordinate[1]][2]==rgbList[2]):
        return True
for x in range(imgRGB.size[0]):
    for y in range(imgRGB.size[1]):
        if checkPixRGB(img, [x, y], rgbValue):
            if not (
                checkPixRGB(img, [x-1, y+1], rgbValue) or
                checkPixRGB(img, [x, y+1], rgbValue) or
                checkPixRGB(img, [x+1, y+1], rgbValue) or
                checkPixRGB(img, [x-1, y], rgbValue) or
                checkPixRGB(img, [x+1, y], rgbValue) or
                checkPixRGB(img, [x-1, y-1], rgbValue) or
                checkPixRGB(img, [x, y-1], rgbValue) or
                checkPixRGB(img, [x+1, y-1], rgbValue)):
                img[x,y]=(0,0,0)
imgRGB.save(newFilePath)
oldRaster = gdal.Open(filePath)
newRaster = gdal.Open(newFilePath,1)
pcs=oldRaster.GetProjection()
tsf=oldRaster.GetGeoTransform()
newRaster.SetGeoTransform(tsf)
newRaster.SetProjection(pcs)


#-*-coding:utf-8-*-
import arcpy
arcpy.env.workspace=r"D:/ArcGIS/Default.gdb"
shpFile= "cn_province"

sCursor1 = arcpy.SearchCursor(shpFile)
# for i in sCursor:
#     row = i.shape
#     for j in sCursor1:
#         a = j.shape
#         if (a.touches(row)):
#             print 'a'
#
# for j in sCursor1:
#     a = j.shape
#     for i in sCursor:
#         row = i.shape
#         if (a.touches(row)):
#             print 'b'

for j in sCursor1:
    a = j.shape
    sCursor = arcpy.SearchCursor(shpFile)
    for i in sCursor:
        row = i.shape
        if (a.touches(row)):
            print str(j.BOU2_4M_ID) + " touches " + str(i.BOU2_4M_ID)