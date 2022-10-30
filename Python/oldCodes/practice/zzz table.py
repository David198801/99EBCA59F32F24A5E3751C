import xlwt
import random
book=xlwt.Workbook()
coordinate=book.add_sheet("coordinate")
for row in range(0,10):
    for col in range(0,1):
        coordinate.write(row,col,random.randint(1,100))
    for col in range(1,2):
        coordinate.write(row,col,random.uniform(0.222,9.888))
book.save("D:/1.xls")
