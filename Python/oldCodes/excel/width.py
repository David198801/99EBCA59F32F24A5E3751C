#-*-coding:utf-8-*-
import xlwt
table = xlwt.Workbook()
sheet = table.add_sheet("sheet", cell_overwrite_ok=True)  # 创建表格
# 写入第一行及设定列宽
sheet.write(0, 0, 'STATION')
sheet.col(0).width = 256 * 25