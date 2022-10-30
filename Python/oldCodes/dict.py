#-*-coding:utf-8-*-
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
d['Michael']=92
print d['Michael']
d['June']=80
print d
f = {'Amy':88}
d.update(f)
d.update({'Sam':77})
d.update(Sam2=77)
print d
del d['Michael'] # 删除键是'Name'的条目
print d
d.clear()    # 清空词典所有条目
del d         # 删除词典
