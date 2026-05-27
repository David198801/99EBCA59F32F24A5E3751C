import os
import json
from openpyxl import Workbook

# 创建工作簿和工作表
wb = Workbook()
ws = wb.active

# 获取指定目录下所有以 .json 结尾的文件
directory = './files/'
json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

first = True
d = {}
# 遍历 JSON 文件并解析数据
for json_file in json_files:
    j = None
    print(json_file)
    with open(os.path.join(directory, json_file), 'r',encoding="UTF-8") as file:
        j = json.load(file)
    #data = j['data']
    data = j
    if first:
        for row in data:
            l=[]
            i=0
            for field in row:
                l.append(field)
                d[field]=i
                i+=1
            ws.append(l)
            break
        first = False
    # 获取 "data" 属性，并写入工作表中
    for row in data:
        l=[None]*len(d)
        for field in row:
            l[d[field]]=row[field]
        ws.append(l)
        
# 保存工作簿
wb.save('output.xlsx')
