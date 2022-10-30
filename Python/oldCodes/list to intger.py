l=range(10)
z=0
for i in range(10):
    z=z+l[-i]*pow(10,i-1)
z=int(z)
print z



'''
import string
l=range(10)
for i in range(10):
    l[i]=str(l[i])
s = ''.join(l)
s = int(s)
print l,s
'''

'''
l=range(10)
l=map(str,l)
sl=''
for i in range(10):
    sl=sl+l[i]
sl = int(sl)
print sl
'''

'''
l=range(10)
l=map(str,l)
def add(x,y):
    return  x+y
sl=reduce(add,l)
print sl
'''
