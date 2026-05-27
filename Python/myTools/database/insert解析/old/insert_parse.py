from sql_metadata import Parser
import tkinter as tk
from tkinter import ttk

def parse_insert_query_and_update_table():
    # 从 Entry 中获取 SQL 查询语句
    sql = entry_input.get().strip()
    # 使用解析器解析 INSERT 查询，并输出到表格中
    try:
        p = Parser(sql)
        column_values = p.values_dict
        table.delete(*table.get_children())
        for column, value in column_values.items():
            table.insert("", tk.END, values=(column, value))
    except Exception as ex:
        print(ex)

# 创建一个窗口和两个控件：Entry 和表格
window = tk.Tk()
entry_input = tk.Entry(window, font=("Arial", 16))
btn_parse = tk.Button(window, text="解析", font=("Arial", 16), command=parse_insert_query_and_update_table)
table = ttk.Treeview(window, columns=("Column", "Value"), show="headings")
table.heading("Column", text="Column")
table.heading("Value", text="Value")

# 设置表格的列宽和样式
table.column("Column", width=200, anchor="center")
table.column("Value", width=200, anchor="center")
table.configure(height=5)

# 将控件添加到窗口中，并设置布局
entry_input.pack(fill=tk.BOTH, padx=10, pady=10)
btn_parse.pack(fill=tk.BOTH, padx=10, pady=10)
table.pack(fill=tk.BOTH, expand=True, padx=10)

# 启动窗口消息循环
window.mainloop()
