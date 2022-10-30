def prime(n):
    if n<=1:
        return True
    for i in range (2,n):
        if n%i==0:
            return True
    return False
print filter(prime,range(1,102))