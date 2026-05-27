import win32clipboard
import win32con

win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
a = data.replace('\\','/') + "/"
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardData(win32con.CF_TEXT, a)
win32clipboard.CloseClipboard()