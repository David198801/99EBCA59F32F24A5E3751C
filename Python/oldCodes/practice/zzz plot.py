import numpy as np
import matplotlib.pyplot as plt
import xlrd
book = xlrd.open_workbook('D:\\coordinate.xls')
coordinate = book.sheet_by_name("coordinate")
x = coordinate.col_values(0)
y = coordinate.col_values(1)
z1 = np.polyfit(x, y, 5)
p1 = np.poly1d(z1)
plt.plot(x, y, 'o')
plt.plot(p1)
plt.show()