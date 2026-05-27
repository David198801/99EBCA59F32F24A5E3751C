import requests
import time

url1 = r"https://www.bluegq.com/"

headers1 = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"cache-control":"max-age=0",
"cookie":"Kd9U_2132_connect_is_bind=0; c=Cbo8VSyL-1586954217155-2ca5171949dd71098827056; Kd9U_2132_saltkey=EU0uZ8tB; Kd9U_2132_lastvisit=1594037437; Kd9U_2132_auth=d1cbIBSS8%2FgqZc6XT7X%2FG9GjDyJgEYnXb%2FeYuBhFIAi8%2BNgRU0JWj0dhYM3mftD0ZTZQ7eA6YGlCt1u8QNSgku7d; Kd9U_2132_lastcheckfeed=2992%7C1594041051; Kd9U_2132_smile=1D1; Kd9U_2132_nofavfid=1; Kd9U_2132_sid=XjgjuS; Kd9U_2132_security_cookiereport=8d56%2F85R3cwpCJCQnS1chcLSLdgf8wSKaZaNAKkHdephfIjeL43v; Kd9U_2132_st_p=2992%7C1594728368%7C3dc093ee8e88eb9e99a093c50bf8e279; Kd9U_2132_visitedfid=67D40D71D100D77D54D68D79; Kd9U_2132_viewid=tid_22979; PHPSESSID=3r0icg750i84um4n36f6fpmab0; Kd9U_2132_ulastactivity=1bc8r7gr8vekr0HJLN05BA6oMtWAcSgb2KTx1hjJag6f8KzajvkH; Kd9U_2132_sendmail=1; Kd9U_2132_seccode=2181.5cb0ad4a5d952ab407; Kd9U_2132_onlineusernum=401; _fmdata=OgbcnEy%2F02RGilOVeDhi2umd7r1WWTJgp4OSH8SLFz7GY4tLDTTvMgTUVm%2Fj6nUTnETGNZjLTchOKd3G7Sl0eW4FURfZvhpVpFhO%2BQBpZj4%3D; _xid=ayJVItv3zTc6FNvqCfyX83qvJfW8TnAYG%2FGz105SA5dxRCY5HAJBMrArtPNryfDUFlb79aN%2BCG%2B1sFSz7oQf8g%3D%3D; Kd9U_2132_lastact=1594728393%09plugin.php%09; Kd9U_2132_creditnotice=0D0D60D0D0D0D0D0D0D2992; Kd9U_2132_creditbase=0D0D1088D686D0D0D0D0D0",
"sec-fetch-mode":"navigate",
"sec-fetch-site":"same-origin",
"sec-fetch-user":"?1",
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

time.sleep(1)

url2 = r"https://www.bluegq.com/plugin.php?id=fx_checkin:checkin&formhash=ff5e9d28&ff5e9d28&infloat=yes&handlekey=fx_checkin&inajax=1&ajaxtarget=fwin_content_fx_checkin"

headers2 = {'accept': '*/*',
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"cookie":"Kd9U_2132_connect_is_bind=0; c=Cbo8VSyL-1586954217155-2ca5171949dd71098827056; Kd9U_2132_saltkey=EU0uZ8tB; Kd9U_2132_lastvisit=1594037437; Kd9U_2132_auth=d1cbIBSS8%2FgqZc6XT7X%2FG9GjDyJgEYnXb%2FeYuBhFIAi8%2BNgRU0JWj0dhYM3mftD0ZTZQ7eA6YGlCt1u8QNSgku7d; Kd9U_2132_lastcheckfeed=2992%7C1594041051; Kd9U_2132_smile=1D1; Kd9U_2132_nofavfid=1; Kd9U_2132_sid=XjgjuS; Kd9U_2132_security_cookiereport=8d56%2F85R3cwpCJCQnS1chcLSLdgf8wSKaZaNAKkHdephfIjeL43v; Kd9U_2132_st_p=2992%7C1594728368%7C3dc093ee8e88eb9e99a093c50bf8e279; Kd9U_2132_visitedfid=67D40D71D100D77D54D68D79; Kd9U_2132_viewid=tid_22979; PHPSESSID=3r0icg750i84um4n36f6fpmab0; Kd9U_2132_ulastactivity=1bc8r7gr8vekr0HJLN05BA6oMtWAcSgb2KTx1hjJag6f8KzajvkH; Kd9U_2132_sendmail=1; Kd9U_2132_checkpm=1; Kd9U_2132_seccode=2181.5cb0ad4a5d952ab407; Kd9U_2132_onlineusernum=401; _fmdata=OgbcnEy%2F02RGilOVeDhi2umd7r1WWTJgp4OSH8SLFz7GY4tLDTTvMgTUVm%2Fj6nUTnETGNZjLTchOKd3G7Sl0eW4FURfZvhpVpFhO%2BQBpZj4%3D; _xid=ayJVItv3zTc6FNvqCfyX83qvJfW8TnAYG%2FGz105SA5dxRCY5HAJBMrArtPNryfDUFlb79aN%2BCG%2B1sFSz7oQf8g%3D%3D; Kd9U_2132_lastact=1594728374%09misc.php%09patch",
"referer":"https//www.bluegq.com/",
"sec-fetch-mode":"cors",
"sec-fetch-site":"same-origin",
"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
"x-requested-with":"XMLHttpRequest"}

requests.get(url1,headers=headers1)
requests.get(url2,headers=headers2)