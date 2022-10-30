#coding:utf8
from win32com.client import DispatchEx

paperPath = "C:/Users/admin/Desktop/test.docx"

wordApp = DispatchEx('Excel.Application')

# with open("C:/Users/admin/Desktop/test.txt") as txt:
#     code = txt.read().splitlines()
#
# code = [i[:3] for i in code]