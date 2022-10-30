import requests
import time

url = r"https://www.panle.net/plugin.php?id=dsu_amupper&ppersubmit=true&formhash=b486f3a2&infloat=yes&handlekey=dsu_amupper&inajax=1&ajaxtarget=fwin_content_dsu_amupper"

headers = {"accept":"*/*",
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
"cookie":"IjIR_2132_connect_is_bind=1; IjIR_2132_nofavfid=1; IjIR_2132_study_nge_extstyle=auto; IjIR_2132_study_nge_extstyle_default=auto; IjIR_2132_smile=5D1; IjIR_2132_saltkey=Bsmt6j87; IjIR_2132_lastvisit=1599374715; IjIR_2132_ulastactivity=dd2aQOOaqGHE2EH28xdC%2FDoQyhM5ScqHqEptH%2B%2BL%2FRly36kvklCh; IjIR_2132_auth=58b3EBFnmAWWBir%2BeYNjQvV40zMf6QJJo8y2qfbWXifhVxJBoafJRwlnm%2BkeDCsvFEPPbl4ALt8UH3bRV6ysEf%2BG5mc; IjIR_2132_lastcheckfeed=318174%7C1599378328; IjIR_2132_atarget=1; IjIR_2132_forum_lastvisit=D_71_1599390752D_133_1599390872D_140_1599390904D_50_1599390952D_43_1599390983D_64_1599391070D_55_1599396324D_89_1599402601; IjIR_2132_visitedfid=89D129D55D53D62D37D50D64D43D140; IjIR_2132_dsu_amupper=DQo8c3R5bGU%2BDQoucHBlcndibSB7cGFkZGluZzo2cHggMTJweDtib3JkZXI6MXB4IHNvbGlkICNDRENEQ0Q7YmFja2dyb3VuZDojRjJGMkYyO2xpbmUtaGVpZ2h0OjEuOGVtO2NvbG9yOiMwMDMzMDA7d2lkdGg6MjAwcHg7b3ZlcmZsb3c6aGlkZGVufQ0KLnBwZXJ3Ym0gLnRpbWVze2NvbG9yOiNmZjk5MDA7fQ0KLnBwZXJ3Ym0gIGF7ZmxvYXQ6cmlnaHQ7Y29sb3I6I2ZmMzMwMDt0ZXh0LWRlY29yYXRpb246bm9uZX0NCjwvc3R5bGU%2BDQoNCjxkaXYgY2xhc3M9InBwZXJ3Ym0iIGlkPSJwcGVyd2JfbWVudSIgc3R5bGU9ImRpc3BsYXk6IG5vbmUiID4NCg0KPHN0cm9uZz7ntK%2ForqHnrb7liLA8c3BhbiBjbGFzcz0idGltZXMiPjI8L3NwYW4%2B5qyhPC9zdHJvbmc%2BPGJyPg0KDQo8QSBIUkVGPSJmb3J1bS5waHA%2FbW9kPXZpZXd0aHJlYWQmYW1wO3RpZD0xODA4MzcmYW1wO2F1dGhvcmlkPTMxODE3NCIgdGFyZ2V0PSJfYmxhbmsiPuafpeeci%2BetvuWIsOWbnuW4ljwvQT4NCg0KPHN0cm9uZz7ov57nu63nrb7liLA8c3BhbiBjbGFzcz0idGltZXMiPjA8L3NwYW4%2B5qyhPC9zdHJvbmc%2BPGJyPg0KDQo8c3Ryb25nPuS4iuasoeetvuWIsDogPHNwYW4gY2xhc3M9InRpbWVzIj4yMDIwLTA5LTA2IDE5OjMyOjIwPC9zcGFuPjwvc3Ryb25nPg0KPC9kaXY%2BDQo%3D; IjIR_2132_sendmail=1; IjIR_2132_checkpm=1; IjIR_2132_sid=v8422N; IjIR_2132_lip=140.240.21.10%2C1599454193; IjIR_2132_lastact=1599454194%09misc.php%09patch",
"referer":"https//www.panle.net/",
"sec-fetch-mode":"cors",
"sec-fetch-site":"same-origin",
"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
"x-requested-with":"XMLHttpRequest"}



requests.get(url,headers=headers)