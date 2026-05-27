import requests
import time

url = r"https://bbs.saraba1st.com/2b/forum.php"

headers = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"cookie":"_uab_collina=158433000622956570709096; B7Y9_2132_nofavfid=1; B7Y9_2132_smile=1465D1; B7Y9_2132_saltkey=kICyU7y7; B7Y9_2132_lastvisit=1592821029; __cfduid=d8858d98c8aa0538526f0f83687f859be1592824634; B7Y9_2132_visitedfid=6D136D4; B7Y9_2132_sendmail=1; B7Y9_2132_pc_size_c=0; B7Y9_2132_ulastactivity=3930FrQPSWYwQxcl2O7vcX0hfIGqfk7LocgZY%2FKoGUwnoI943sWs; B7Y9_2132_auth=98efQc00PbDXTt0SV0NagYfzmS0KMN4xg7c%2FWy0JJIxGA1n7ygkVWn%2FScAC%2F0rIfumeIobPyNctMwCcqUqyKQi0B5h8; B7Y9_2132_lastcheckfeed=463089%7C1593936467; B7Y9_2132_checkfollow=1; B7Y9_2132_yfe_in=1; B7Y9_2132_myrepeat_rr=R0; B7Y9_2132_checkpm=1; B7Y9_2132_home_diymode=1; B7Y9_2132_sid=SeD9Qk; B7Y9_2132_lip=123.207.14.250%2C1593936483; B7Y9_2132_lastact=1593936488%09home.php%09spacecp",
"referer":"https//bbs.saraba1st.com/2b/home.php?mod=spacecp&ac=usergroup",
"sec-fetch-mode":"navigate",
"sec-fetch-site":"same-origin",
"sec-fetch-user":"?1",
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}



while True:
    r = requests.get(url,headers = headers)
    time.sleep(30)