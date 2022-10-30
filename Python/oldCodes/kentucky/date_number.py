import datetime
date_number=[]
d_begin = datetime.date(2008,1,1)
d_end = datetime.date(2017,9,1)
d_days = d_begin
delta = datetime.timedelta(days=1)
while d_days <= d_end:
    date_number.append(d_days.strftime("%Y%m%d"))
    d_days += delta