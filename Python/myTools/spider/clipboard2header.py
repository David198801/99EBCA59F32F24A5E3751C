import win32clipboard
import win32con

def get_text():
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return text
def set_text(string):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
    win32clipboard.CloseClipboard()


text = get_text()

clipList = text.split("\r\n")

newClip = ""
for i in clipList:
    h = i.split(":")
    if h[0] == "":
        h = h[1:]
        h[0] = ":" + h[0]
    if len(h)>2:
        h[1] = "".join(h[1:])
        h = h[:2]
    h[1] = h[1][1:]
    line = '''"''' + h[0] + '''"''' + ":" + '''"''' + h[1] + '''"''' + ",\n"
    if '\"\"' in line:
        line = line.replace('\"\"',"\'\'\'\"").replace("\'\'\'\",","\"\'\'\',")
    newClip += line

newClip = "{" + newClip[:-2] + "}"
print(newClip)
set_text(newClip)