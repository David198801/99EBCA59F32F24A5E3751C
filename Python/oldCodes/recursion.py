def fact_iter(num, product=1):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)
i=fact_iter(6)
print i
