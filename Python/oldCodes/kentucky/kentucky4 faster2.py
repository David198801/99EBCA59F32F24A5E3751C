#-*-coding:utf-8-*-
import os
import xlwt
import xlrd
from xlutils.copy import copy
import datetime
#输出连续日期的set
date_number=set([])
d_begin = datetime.date(2008,1,1)
d_end = datetime.date(2017,9,1)
d_days = d_begin
delta = datetime.timedelta(days=1)
while d_days <= d_end:
    date_number.add(d_days.strftime("%Y%m%d"))
    d_days += delta
filenames_data=os.listdir('D:/ghcnd_all/USC0015')#获取目录下所有文件
#获取所需数据
need_data={}
for a in range(2008, 2018):#遍历2008到2017年
    yearDict = set([])
    for h in filenames_data:  # 遍历每一个气象站（文件）数据
        data_file = open('D:/ghcnd_all/USC0015/' + h)  # 打开某个数据文件
        all_data = data_file.readlines()  # 读取每一行
        for b in all_data:  # 获取当前年分数据并写入need_data
            if h[0:11] + str(a) in b:
                yearDict.add(b)
    need_data[str(a)] = yearDict
for i in date_number:#遍历每日
    table = xlwt.Workbook()
    sheet = table.add_sheet("sheet",cell_overwrite_ok=True)#创建表格
    #写入第一行及设定列宽
    sheet.write(0, 0, 'STATION')
    sheet.col(0).width = 256 * 25
    sheet.write(0, 1, 'STATE')
    sheet.col(1).width = 256 * 10
    sheet.write(0, 2, 'STATION_NAME')
    sheet.col(2).width = 256 * 25
    sheet.write(0, 3, 'ELEVATION')
    sheet.col(3).width = 256 * 15
    sheet.write(0, 4, 'LATITUDE')
    sheet.col(4).width = 256 * 12
    sheet.write(0, 5, 'LONGTUDE')
    sheet.col(5).width = 256 * 12
    sheet.write(0, 6, 'DATE')
    sheet.col(6).width = 256 * 10
    sheet.write(0, 7, 'TMAX')
    sheet.col(7).width = 256 * 10
    sheet.write(0, 8, 'TMIN')
    sheet.col(8).width = 256 * 10
    sheet.write(0, 9, 'TOBS')
    sheet.col(9).width = 256 * 10
    sheet.write(0, 10, 'SNOW DEPTH')
    sheet.col(10).width = 256 * 15
    sheet.write(0, 11, 'PRECIPATION')
    sheet.col(11).width = 256 * 15
    m_day = (int(i[-2:]) - 1) * 8#设定每日数据在每行中的间隔
    for j in range(len(filenames_data)):  # 遍历每一个文件
        # 获取当前月数据
        month_data = []
        for l in need_data[str(i[0:4])]:
            if filenames_data[j][0:11] + i[0:6] in l:
                month_data.append(l)
        for m in month_data:  # 遍历本月每一个数据
            def writeData(da_name, da_col):  # d定义写入函数
                if filenames_data[j][0:11] + i[0:6] + da_name in m:
                    if m[(21 + m_day):(26 + m_day)] == '-9999':  # 检查无效值
                        pass
                    else:
                        sheet.write(j + 1, da_col, float(m[(21 + m_day):(26 + m_day)]))
            # 写入数据
            writeData('TMAX', 7)
            writeData('TMIN', 8)
            writeData('TOBS', 9)
            writeData('SNWD', 10)
            writeData('PRCP', 11)
        sheet.write(j + 1, 0, 'GHCND:' + filenames_data[j][0:11])  # 写入第1列
        sheet.write(j + 1, 1, 'Kentucky')  # 写入第2列
        meta_data_file = open('D:/ghcnd_all/ghcnd-stations.txt')  # 读取ghcnd-stations.txt数据
        all_meta_data = meta_data_file.readlines()
        for n in all_meta_data:  # 遍历每一行
            if filenames_data[j][0:11] in n:  # 查找当前气候站数据
                # #写入高程、经纬度、日期
                sheet.write(j + 1, 2, n[41:71])
                sheet.write(j + 1, 3, float(n[31:37]))
                sheet.write(j + 1, 4, float(n[12:20]))
                sheet.write(j + 1, 5, float(n[21:30]))
                sheet.write(j + 1, 6, i)
                if n[76:79] == 'HCN':  # 检查HCN标签并覆写
                    sheet.write(j + 1, 0, 'GHCND:' + filenames_data[j][0:11] + ' HCN')
    file_name=i
    table.save("D:/python/kentucky/"+file_name+".xls")# 按日确定文件名并保存
    #检查空单元格并写入NoData并覆盖文件(xlwt无法直接修改表格)
    checkbook = xlrd.open_workbook("D:/python/kentucky/"+file_name+".xls",formatting_info=True)
    checksheet = checkbook.sheet_by_index(0)
    changebook = copy(checkbook)
    changesheet = changebook.get_sheet(0)
    for x in range(checksheet.nrows):
        for y in range(checksheet.ncols):
            if checksheet.cell(x, y).ctype == 0:
                changesheet.write(x, y, 'NoData')
    changebook.save("D:/python/kentucky/" + file_name + ".xls")