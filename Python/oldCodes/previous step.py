i=1
back='back'
while(True):
    if i == 1:
        i1 = raw_input("enter 1 ")
        i = i + 1
    elif i == 2:
        i2 = raw_input("enter 2 ")
        if i2 == back:
            i = i - 1
        else:
            i = i + 1
    elif i == 3:
        i3 = raw_input("enter 3 ")
        if i3 == back:
            i = i - 1
        else:
            i = i + 1
    elif i == 4:
        i4 = raw_input("Please enter \"done\" to done\n")
        if i4 == back:
            i = i - 1
        else:
            break
'''          
    elif i == back:
        pass
    else:
        break
'''
print i1
print i2
print i3