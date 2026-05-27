c=raw_input('enter charactors:')
n=len(c)
n1=1
n2=3
if n<3:
    print 'error'
else:
    while n2 < n:
        n2=n2+1
        while n1 < n2:
            n1=n1+1
            if 2*n1+n2==n+2:
                print n,n1,n2
