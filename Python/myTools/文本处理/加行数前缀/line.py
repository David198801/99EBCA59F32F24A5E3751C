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
    
def add_line_prefix(input_str):
    lines = input_str.splitlines()  # 将字符串分割为行列表[6,7](@ref)
    new_lines = []
    for idx, line in enumerate(lines, start=1):  # 行号从1开始[9,10](@ref)
        formatted_idx = f"{idx:02d}"  # 行号补零至2位（如1→"01"）[1,3](@ref)
        new_lines.append(f"{formatted_idx}_{line}")  # 添加前缀并保留原内容
    return "\n".join(new_lines)  # 重新组合为字符串[6](@ref)

def func():
    input("请按回车：\n")
    input_str = get_text()
    outputStr = add_line_prefix(input_str)
    set_text(outputStr)
    print(outputStr)

while True:
    func()