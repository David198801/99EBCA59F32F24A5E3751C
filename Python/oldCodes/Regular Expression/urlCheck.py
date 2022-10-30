import re
pattern2 = re.compile(r'((?!http://).+/.+/.*)|(http://.+/.+/.*)')
# pattern1 = re.compile(r'^[^\?]+$')
pattern1 = re.compile(r'^.+\?.+$')
l=['militia.info/',
'www.apcnc.com.cn/',
'http://www.cyjzs.com/',
'www.greena888.com/',
'www.800cool.net/',
'http://hgh-products.my-age.net/',
'thursdaythree.net/greenhouses--gas-global-green-house-warming/',
'http://www.mw.net.tw/user/tgk5ar1r/profile/',
'http://www.szeasy.com/food/yszt/chunjie/',
'www.fuckingjapanese.com/Reality/',
'www.buddhismcity.net/utility/mailit.php?l=/activity/details/3135/',
'www.buddhismcity.net/utility/mailit.php?l=/activity/details/2449/']
for u in l:
    p1=pattern1.match(u)
    p2=pattern2.match(u)
    if p1:
    #     if p2:
    #         print 'subPage ' + u
    #     else:
    #         print 'mainPage ' + u
    # else:
        print 'otherPage ' + u