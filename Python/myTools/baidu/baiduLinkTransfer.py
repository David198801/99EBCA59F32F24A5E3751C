import base64

def mengji2pandl(link):
  l = link.lower().split("#")
  real = l[3] + "|" + l[2] + "|" + l[0] + "|" + l[1]
  b = base64.b64encode(real.encode("utf8"))
  pandl = "bdpan://" + b.decode()
  return pandl


def pandl2mengji(link):
  p = link.replace("bdpan://","")
  real = base64.b64decode(p).decode("utf8")
  l = real.split("|")
  mengji = l[2].upper() + "#" + l[3].upper() + "#" +l[1].upper() + "#" + l[0]
  return mengji

#print(mengji2pandl(k1))
#print(pandl2mengji(k2))

k1 = "8884920E69573AB520D576A215CAE569#A12EC981162B4CBBF61D492245F0A488#32170824#夢路らびりんす ~千矢ver.~.flac"

k2 = "bdpan://44CMMDHjgI0ucmFyfDU3NDA3MTUzNnxiNmE1NTczZjk1MTEyZWQ2NmU1NzE1ZDRlMDQ4MzIyZnxlZTAyOTJlNmY2YzUyMzA4ZGNjZTM3ZjZlNzYyMzUyMw=="

print(mengji2pandl(k1))
print(pandl2mengji(k2))