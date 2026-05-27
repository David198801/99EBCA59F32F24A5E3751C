age = int(raw_input('please enter your age:'))
if age >= 18:
    print 'adult'
else:
    print 'teenager'

'''
或者age = input('please enter your age:')
if age >= 18:
    print 'adult'
else:
    print 'teenager'

都是可以的，不嫌代码繁琐，还可以：
age = raw_input('please enter your age:')
age=int(age)
if age >= 18:
    print 'adult'
else:
    print 'teenager'
'''