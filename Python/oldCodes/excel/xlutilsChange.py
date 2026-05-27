#-*-coding:utf-8-*-
import xlwt
import xlrd
from xlutils.copy import copy
table = xlwt.Workbook()
sheet = table.add_sheet("sheet",cell_overwrite_ok=True)#创建表格
#省略写入表格
checkbook = xlrd.open_workbook("D:/python/kentucky/" + file_name + ".xls", formatting_info=True)
checksheet = checkbook.sheet_by_index(0)
changebook = copy(checkbook)
changesheet = changebook.get_sheet(0)
for x in range(checksheet.nrows):
    for y in range(checksheet.ncols):
        if checksheet.cell(x, y).ctype == 0:
            changesheet.write(x, y, 'NoData')
changebook.save("D:/python/kentucky/" + file_name + ".xls")