# -*- coding: utf-8 -*-
import os
l1 = [x*x*x for x in range(1,10)]
l2 = [x*x for x in range(1,10) if x%3==0]
l3=[m + n for m in 'ABC' for n in 'XYZ']
d = {'x': 'A', 'y': 'B', 'z': 'C' }
l4= [k + '=' + v for k, v in d.iteritems()]
files=[d for d in os.listdir('.')] # os.listdir可以列出文件和目录
print l1
print l2
print l3
print l4
print files