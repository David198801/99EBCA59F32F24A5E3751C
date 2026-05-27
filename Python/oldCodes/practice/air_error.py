#coding:utf-8
import os
import csv
import shapefile

InputPath = r"E:/BaiduNetdiskDownload/china_sites/"
OutPath = r"E:/BaiduNetdiskDownload/china_sites_shp/"

years=['2014','2015','2016','2017','2018']
Month = ['01', '02',  '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
Days = ['01', '02',  '03', '04', '05', '06', '07', '08', '09', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']


aaaaa = 0

for indexY in years:
    for indexM in Month:
        for indexD in Days:
            in_file = InputPath + "china_sites_" + indexY + indexM + indexD + ".csv"
            if os.path.exists(in_file):
                with open(in_file) as csv_first:
                    rows = csv.reader(csv_first)
                    first_row = list(rows)[0]

                with open(in_file) as csvFile:
                    rows = csv.reader(csvFile)
                    next(rows)
                    count_rows = 0
                    for index_rows in rows:
                        out_file = OutPath + "china_sites_" + index_rows[0] + index_rows[1].zfill(2) + ".shp"
                        count_rows += 1
                        if count_rows % 15 == 1:
                            shp = shapefile.Writer(shapeType=1)
                            shp.autoBalance = 1
                            shp.field('city', 'C', '20')
                            shp.field('site', 'C', '30')
                        shp.field(index_rows[2], 'C', '12')
                        if count_rows % 15 == 0:
                            shp.save(out_file)


                    site_dict = []
                    for col in range(len(first_row) - 3):
                        with open(r"E:/BaiduNetdiskDownload/site_list.csv") as site_list:
                            site_rows = csv.reader(site_list)
                            next(site_rows)
                            for index_site in site_rows:
                                site_info = []
                                if first_row[col + 3] == index_site[0]:
                                    site_info.append(float(index_site[3]))
                                    site_info.append(float(index_site[4]))
                                    site_info.append(index_site[1])
                                    site_info.append(index_site[2])
                                    site_dict.append(site_info)
                                    # longitude = float(index_site[3])
                                    # latitude = float(index_site[4])
                                    # station_name = index_site[1]
                                    # city_name = index_site[2]
                                    # shp_path = r"E:/BaiduNetdiskDownload/china_sites_shp/"
                                    # list_dir = os.listdir(shp_path)
                                    # for files in list_dir:
                                    #     if files[-3:] == 'shp':
                                    #         shp = shapefile.Editor(shp_path + files)
                                    #         shp.point(longitude, latitude,0,0)
                                    #         shp.save(shp_path + files)
                                    #         print longitude, latitude, files
                    count_shps = 0
                    shp_path = r"E:/BaiduNetdiskDownload/china_sites_shp/"
                    list_dir = os.listdir(shp_path)
                    for files in list_dir:
                        if files[-3:] == 'shp':
                            count_shps += 1
                            count_rows = 0
                            shp = shapefile.Editor(shp_path + files)
                            for site_num in range(len(site_dict)):
                                shp.point(site_dict[site_num][0], site_dict[site_num][1], 0, 0)
                                # shp.save(shp_path + files)

                                # count_rows = 0
                                # for index_rows in rows:
                                #     out_file = OutPath + "china_sites_" + index_rows[0] + index_rows[1].zfill(2) + ".shp"
                                #     shp = shapefile.Editor(out_file)
                                #     shp.record(index_rows[col + 3], index_rows[2])
                                #     count_rows += 1
                                #     if count_rows % 15 == 0:
                                #         shp.save(out_file)
                                # count_rows = 0
                                with open(in_file) as csvFile:
                                    rows2 = csv.reader(csvFile)
                                    next(rows2)
                                    for index_rows in rows2:
                                        count_rows += 1
                                        if (count_rows < count_shps * 15 and count_rows >= (count_shps-1)*15):
                                            for index_cols in range(len(index_rows) - 3):
                                                if index_cols == site_num:
                                                    # shp.record(index_rows[2], index_rows[index_cols + 3])
                                                    print index_rows[2], index_rows[index_cols + 3]
                                                    aaaaa += 1
                                                    print aaaaa,count_shps,count_rows
                            # shp.save(shp_path + files)