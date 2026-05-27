def fib(n):
    i=0
    a=0
    b=1
    while i<n:
        i=i+1
        print b
        temp=a
        a=b
        b=temp+b


def fib_better(max):
    n, a, b = 0, 0, 1
    while n < max:
        print b
        a, b = b, a + b
        n = n + 1

fib(8)
fib_better(8)