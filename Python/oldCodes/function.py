def add_function(a,b):
    c = a+b
    print c
add_function(2,3)

def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print calc(1,2,3,4,5,6,7)
a=(1,2,3)
print calc(*a)

def person(name, age, **kw):
    print 'name:', name, 'age:', age, 'other:', kw
person('m',30)