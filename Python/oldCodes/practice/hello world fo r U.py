import sys
c=raw_input('enter charactors:')
n=len(c)
i = 0
k = 0
max=-1
if n<3:
    print 'error'
else:
    n2 = 3
    while n2 <= n:
        n2=n2+1
        n1=1
        while n1 <= n2:
            n1=n1+1
            if 2*n1+n2==n+2:
                if max<n1:
                    max=n1
n1=max
n2=n+2-2*n1
while i < n1 - 1:
    i = i + 1
    sys.stdout.write('%s' % c[i - 1])
    j = 0
    while j < n2 - 2:
        j = j + 1
        sys.stdout.write(' ')
    sys.stdout.write('%s\n' % c[n - i])
while k < n2:
    k = k + 1
    sys.stdout.write('%s' % c[n1 + k - 2])
