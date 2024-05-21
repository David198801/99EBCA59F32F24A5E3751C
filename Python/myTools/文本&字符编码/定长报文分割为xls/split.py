import xlwt


l = [2,8,12,6,3,36,16,16,16,16,16,16,16,16,16,16,1,1,16,16,16,16]

path = "a.txt"
output_path = "output.xls"

# 读取文件
with open(path, 'r', encoding='utf-8') as file:
    lines = [x.replace('\n','') for x in file.readlines()]

# 创建一个新的工作簿和一个工作表
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Sheet1')

rownum=0

# CSV头部
headers = [f's{i}' for i in range(len(l))]
for colnum, data in enumerate(headers):
    sheet.write(rownum, colnum, data)
rownum+=1

# 处理每一行并写入CSV文件
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    datas=[]
    for line in lines:
        encoded_line = line.encode('gbk')
        print(encoded_line)
        print(len(encoded_line))
        row = []
        start = 0
        for i in l:
            row.append(encoded_line[start:start+i])
            start+=i
        row = [x.decode('gbk', errors='ignore') for x in row]
        for colnum, data in enumerate(row):
            sheet.write(rownum, colnum, data)
        rownum+=1
        
# 保存工作簿到文件
workbook.save(output_path)