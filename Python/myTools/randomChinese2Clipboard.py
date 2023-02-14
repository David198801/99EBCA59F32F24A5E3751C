import random
import win32clipboard
import win32con

def set_text(string):
  win32clipboard.OpenClipboard()
  win32clipboard.EmptyClipboard()
  win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
  win32clipboard.CloseClipboard()

txtPath = r"../../others/3500个常用汉字列表.txt"

n = 5

c = ""
with open(txtPath,"r",encoding="utf-8-sig") as txt:
  chinese = txt.read()
  l = len(chinese)
  for i in range(n):
    r = random.randint(0,l-1)
    c += chinese[r]
  set_text(c)
