# -*- coding: utf-8 -*-
mon=[31,28,31,30,31,30,31,31,30,31,30,31]
year=input("Year=")
if year%4==0:
    mon[1]=29
print "Enter 'quit' to quit"
quit='quit'
while(True):
    days = input("Days?\n")
    s = 0
    if days==quit:
        print "Done"
        break
    for i in range(12):
        mon_days = days - s
        s = s + mon[i]
        if days <= s:
            print u"%d m %d d" % (i + 1, mon_days)
            break
