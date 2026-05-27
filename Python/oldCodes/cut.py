#list[start:stop+1:step]
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print l[0:3] # = print l[0:3:1]
print l[:3] # = print l[0:3:1]
print l[1:3] # = print l[1:3:1]
print l[-3:10] # = print l[-3:10:1]
print l[-3:] # = print l[-3:len(l):1]
print l[-3:-1] # = print l[-3:-1:1]
print l[:] # = print l[0:len(l):1]
print l[-1:0:-1]
l_100=range(101)
print l_100[::5] # = print l[0:len(l):5]
print l_100[::-5] # reverse