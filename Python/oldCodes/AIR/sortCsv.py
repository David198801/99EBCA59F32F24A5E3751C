# coding:utf-8
import pandas as pd
import os
a=os.listdir(r"D:\air\2017")
p="D:\\air\\2017\\"

for i in a:
    if i[-3:]=="csv":
        df = pd.DataFrame(pd.read_csv(p + i, encoding="gbk", low_memory=False, index_col="updatetime"))
        df.index = pd.DatetimeIndex(df.index)
        a = df.sort_index()
        pd.DataFrame(a).to_csv(p +"sort\\"  + i, encoding="gbk")