# coding:utf-8
import re

page_file = open(ur'C:/Users/admin/Desktop/美剧《硅谷》的全部资源下载,1天后删除,要看的抓紧时间 —— 来自最帅的资源信息分享站.html')
all_lines = page_file.readlines()

labels_b = []
for i in range(len(all_lines)):
    season_r = re.match(r'.*(第\d季 720P).*', all_lines[i])
    if season_r:
        labels_b.append(i)

labels_e = []
for i1 in labels_b:
    counter = 0
    for i2 in range(i1, len(all_lines)):
        div = re.match(r'.*<div.*>.*', all_lines[i2])
        divE = re.match(r'.*</div>.*', all_lines[i2])
        if div:
            counter += 1
        if divE and counter != 0:
            counter -= 1
            continue
        elif divE and counter == 0:
            labels_e.append(i2)
            break

for i1 in range(len(labels_b)):
    counter = 0
    for i2 in range(labels_b[i1],labels_e[i1]+1):
        ed2k = re.match(r'.*\"(ed2k://.+\|\/)\".*',all_lines[i2])
        if ed2k and counter == 0:
            counter += 1
            print ed2k.group(1)
        elif ed2k and counter != 0:
            counter -= 1
            continue