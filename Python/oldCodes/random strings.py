import random
import string
seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
sa = []
for i in range(8):
    sa.append(random.choice(seed))
salt = ''.join(sa)
print salt

'''
import random
import string
salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
print salt
'''