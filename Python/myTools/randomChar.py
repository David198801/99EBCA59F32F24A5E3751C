import random

a = "abcdefghijklmnopqrstuvwxyz"
b = "abcdefghijklmnopqrstuvwxyz1234567890"
c = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

l=len(a)
l2=len(b)

li = []
for i in range(1000):
  s=""
  r = random.randint(0,l-1)
  s += a[r]
  for j in range(7):
    r = random.randint(0,l2-1)
    s += b[r]
  li.append(s)

with open("a.txt","w") as txt:
  for i in li:
    txt.write(i+"\n")