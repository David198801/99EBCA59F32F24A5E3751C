from collections import Counter #引入Counter
with open(r"D:\account\账号\待下备份\秒传链接\上传待下备份1 共1272.txt",encoding="utf-8") as txt:
    l = [x.replace("\n","") for x in txt.readlines()]
    b = dict(Counter(l))
    for i in b:
        if b[i] > 1:
            print(i)
input()