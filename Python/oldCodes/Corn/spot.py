#-*-coding:utf-8-*-
import arcpy
arcpy.env.workspace=r"D:/kentucky"
shpFile= r"CDL_Corn_2012_PCS.shp"
# fieldList=[]
# fieldAddressList=arcpy.ListFields(shpPath)
# for fieldsAddress in fieldAddressList:
#     fieldList.append(fieldsAddress.aliasName)
minArea=4500
field = "Area"
uCursorMin = arcpy.UpdateCursor(shpFile,'Area<='+str(minArea))
sCursorGreater = arcpy.SearchCursor(shpFile, 'Area>' + str(minArea))
uCursorGreater = arcpy.UpdateCursor(shpFile, 'Area>' + str(minArea))
for minrow in uCursorMin:
    minPolygon=minrow.shape
    adjacentAreas=[]
    for row in sCursorGreater:
        adjacentPolygon = row.shape
        if (minPolygon.touches(adjacentPolygon)):
            adjacentAreas.append(adjacentPolygon.area)
    if len(adjacentAreas)>0:
        maxArea = max(adjacentAreas)
        for row2 in uCursorGreater:
            if (row2.shape.area == maxArea):
                row2.shape = row2.shape.union(minPolygon)
                uCursorGreater.updateRow(row2)
                uCursorMin.deleteRow(minrow)
    # else:
    #     uCursorMin.deleteRow(minrow)