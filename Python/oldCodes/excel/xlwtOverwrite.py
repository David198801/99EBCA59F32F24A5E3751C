#-*-coding:utf-8-*-
import xlwt
table = xlwt.Workbook()
sheet = table.add_sheet("sheet", cell_overwrite_ok=True)  # 创建可覆写表格