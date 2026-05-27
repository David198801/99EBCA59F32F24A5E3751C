# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

def fn(x, y):
    return x * 10 + y
def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
print reduce(fn, map(char2num, '13579'))
print map(char2num, '13579')