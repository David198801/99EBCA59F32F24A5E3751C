names=['adam', 'LISA', 'barT']
print map(str.capitalize,names),names

def prod(i):
    def cheng(x,y):
        return x*y
    return reduce(cheng,i)

print prod([1,2,3,4,5])