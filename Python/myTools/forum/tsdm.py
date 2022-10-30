import requests

url = r'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"s_gkr8_f779_connect_is_bind=0; s_gkr8_f779_styleid=4; s_gkr8_f779_saltkey=OzT1kWIy; s_gkr8_f779_lastvisit=1596512962; s_gkr8_f779_auth=ca4fb6ecYG88FUJdM1PhVMHWQ5dqpCJf%2FCMvqMqYUY%2B9s2rQoiufvPER30R3X2fpngs6Go7Us%2BZ0pmuoD7CnUZ0m4QQ; s_gkr8_f779_smile=12D1; s_gkr8_f779_sid=OMLMio; s_gkr8_f779_ulastactivity=a251EebJsYru%2BEdBHU%2BrWYsAB7QY%2B3yLBdO4kPoSaaSVqmlSfjs0; s_gkr8_f779_sendmail=1; s_gkr8_f779_forum_lastvisit=D_30_1597839703D_17_1598173709D_4_1598253061; s_gkr8_f779_fid4=1598193917; s_gkr8_f779_fid418=1598088632; s_gkr8_f779_visitedfid=418D4D116D6D279D47D247D12D122D17; s_gkr8_f779_lastact=1598253159%09home.php%09spacecp",
"Host":"www.tsdm39.net",
"Referer":"https//www.tsdm39.net/forum.php?mod=forumdisplay&fid=4",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"same-origin",
"Sec-Fetch-User":"?1",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

requests.get(url,headers = headers)

