'''
g = (x * x for x in range(10))
for i in g:
    print i
'''
def fib(n):
    i=0
    a=0
    b=1
    while i<n:
        i=i+1
        yield b
        temp=a
        a=b
        b=temp+b
for i in fib(8):
    print i