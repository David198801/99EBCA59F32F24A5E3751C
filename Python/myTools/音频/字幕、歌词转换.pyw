import os
import sys
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pysubs2
import pylrc

# 拖拽支持
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False


SUPPORTED_INPUTS = [".srt", ".ass", ".ssa", ".vtt", ".lrc"]
SUPPORTED_OUTPUTS = ["srt", "ass", "ssa", "vtt", "lrc"]

WINDOWS_UI_FONT = ("Microsoft YaHei UI", 10)
WINDOWS_UI_FONT_TITLE = ("Microsoft YaHei UI", 15, "bold")


def ms_to_lrc_timestamp(ms: int) -> str:
    """毫秒转 LRC 时间标签 [mm:ss.xx]"""
    if ms < 0:
        ms = 0
    total_centiseconds = ms // 10
    minutes = total_centiseconds // 6000
    seconds = (total_centiseconds % 6000) // 100
    centiseconds = total_centiseconds % 100
    return f"[{minutes:02d}:{seconds:02d}.{centiseconds:02d}]"


def lrc_timestamp_to_ms(line) -> int:
    """将 pylrc 行对象时间转成毫秒"""
    minute = getattr(line, "minute", 0)
    second = getattr(line, "second", 0)
    millisecond = getattr(line, "millisecond", 0)

    if millisecond < 100:
        return minute * 60 * 1000 + second * 1000 + millisecond * 10
    return minute * 60 * 1000 + second * 1000 + millisecond


def strip_extension(path: str) -> str:
    return os.path.splitext(path)[0]


def normalize_dropped_file_path(data: str) -> str:
    """
    处理拖拽进来的路径。
    Windows 拖拽文件可能长这样：
      {C:/xxx/aaa.srt}
    或多个：
      {C:/a.srt} {C:/b.lrc}
    这里只取第一个文件。
    """
    data = data.strip()
    if not data:
        return ""

    files = []

    if data.startswith("{"):
        current = ""
        inside = False
        for ch in data:
            if ch == "{":
                inside = True
                current = ""
            elif ch == "}":
                inside = False
                if current.strip():
                    files.append(current.strip())
            else:
                if inside:
                    current += ch
    else:
        files = data.split()

    return files[0] if files else ""


def convert_lrc_to_subs(lrc_path: str) -> pysubs2.SSAFile:
    """LRC 转 pysubs2 对象"""
    with open(lrc_path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    lrc_obj = pylrc.parse(content)
    subs = pysubs2.SSAFile()

    if not lrc_obj:
        return subs

    for i, line in enumerate(lrc_obj):
        start = lrc_timestamp_to_ms(line)
        text = getattr(line, "text", "") or ""

        if i < len(lrc_obj) - 1:
            end = lrc_timestamp_to_ms(lrc_obj[i + 1])
        else:
            end = start + 3000

        if end <= start:
            end = start + 2000

        subs.append(pysubs2.SSAEvent(start=start, end=end, text=text))

    return subs


def convert_subs_to_lrc(input_path: str, output_path: str):
    """字幕转 LRC"""
    subs = pysubs2.load(input_path)

    lines = []
    for event in subs:
        if event.is_comment:
            continue
        text = event.plaintext.strip()
        if not text:
            continue
        text = text.replace("\n", " ")
        ts = ms_to_lrc_timestamp(event.start)
        lines.append(f"{ts}{text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def convert_subs_events_to_lrc(subs: pysubs2.SSAFile, output_path: str):
    """字幕对象导出为 LRC"""
    lines = []
    for event in subs:
        if event.is_comment:
            continue
        text = event.plaintext.strip().replace("\n", " ")
        if not text:
            continue
        ts = ms_to_lrc_timestamp(event.start)
        lines.append(f"{ts}{text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def convert_file(input_path: str, output_format: str, output_path: str = None) -> str:
    """执行转换"""
    ext = os.path.splitext(input_path)[1].lower().strip(".")
    if output_format.lower() not in SUPPORTED_OUTPUTS:
        raise ValueError(f"不支持的输出格式: {output_format}")

    if output_path is None:
        output_path = f"{strip_extension(input_path)}.{output_format}"

    if ext == "lrc" and output_format != "lrc":
        subs = convert_lrc_to_subs(input_path)
        subs.save(output_path, format_=output_format)
        return output_path

    if ext != "lrc" and output_format == "lrc":
        convert_subs_to_lrc(input_path, output_path)
        return output_path

    if ext == "lrc" and output_format == "lrc":
        subs = convert_lrc_to_subs(input_path)
        convert_subs_events_to_lrc(subs, output_path)
        return output_path

    subs = pysubs2.load(input_path)
    subs.save(output_path, format_=output_format)
    return output_path


class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("字幕/歌词转换工具")
        self.root.geometry("680x420")
        self.root.resizable(False, False)

        self.input_path_var = tk.StringVar()
        self.output_format_var = tk.StringVar(value="lrc")
        self.output_path_var = tk.StringVar()

        self.setup_style()
        self.build_ui()

    def setup_style(self):
        default_font = WINDOWS_UI_FONT

        self.root.option_add("*Font", default_font)

        style = ttk.Style()
        try:
            style.theme_use("vista")
        except Exception:
            pass

        style.configure("TLabel", font=WINDOWS_UI_FONT)
        style.configure("TButton", font=WINDOWS_UI_FONT)
        style.configure("TEntry", font=WINDOWS_UI_FONT)
        style.configure("TCombobox", font=WINDOWS_UI_FONT)
        style.configure("TLabelframe.Label", font=WINDOWS_UI_FONT)
        style.configure("Title.TLabel", font=WINDOWS_UI_FONT_TITLE)

    def build_ui(self):
        title = ttk.Label(self.root, text="字幕 / 歌词 格式转换", style="Title.TLabel")
        title.pack(pady=12)

        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=12, pady=8)

        # 输入文件
        row1 = ttk.Frame(main)
        row1.pack(fill="x", padx=10, pady=8)

        ttk.Label(row1, text="输入文件:", width=10).pack(side="left")
        self.input_entry = ttk.Entry(row1, textvariable=self.input_path_var, width=62)
        self.input_entry.pack(side="left", padx=5)
        ttk.Button(row1, text="浏览", command=self.browse_input).pack(side="left")

        # 拖拽提示
        self.drag_tip = ttk.Label(
            main,
            text="可将 .srt / .ass / .ssa / .vtt / .lrc 文件直接拖入输入框",
            foreground="#666666"
        )
        self.drag_tip.pack(anchor="w", padx=12, pady=(0, 6))

        # 输出格式
        row2 = ttk.Frame(main)
        row2.pack(fill="x", padx=10, pady=8)

        ttk.Label(row2, text="输出格式:", width=10).pack(side="left")
        combo = ttk.Combobox(
            row2,
            textvariable=self.output_format_var,
            values=SUPPORTED_OUTPUTS,
            state="readonly",
            width=12
        )
        combo.pack(side="left", padx=5)
        combo.bind("<<ComboboxSelected>>", self.update_output_path)

        # 输出文件
        row3 = ttk.Frame(main)
        row3.pack(fill="x", padx=10, pady=8)

        ttk.Label(row3, text="输出文件:", width=10).pack(side="left")
        ttk.Entry(row3, textvariable=self.output_path_var, width=62).pack(side="left", padx=5)
        ttk.Button(row3, text="另存为", command=self.browse_output).pack(side="left")

        # 按钮
        row4 = ttk.Frame(main)
        row4.pack(fill="x", padx=10, pady=8)

        ttk.Button(row4, text="开始转换", command=self.run_convert).pack(side="left", padx=5)
        ttk.Button(row4, text="清空日志", command=self.clear_log).pack(side="left", padx=5)

        # 日志框
        log_frame = ttk.LabelFrame(main, text="日志")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = tk.Text(
            log_frame,
            height=14,
            wrap="word",
            font=WINDOWS_UI_FONT
        )
        self.log_text.pack(fill="both", expand=True, padx=6, pady=6)

        self.enable_drag_drop()

        self.log("支持输入格式: " + ", ".join(SUPPORTED_INPUTS))
        self.log("支持输出格式: " + ", ".join(SUPPORTED_OUTPUTS))
        if HAS_DND:
            self.log("拖拽功能已启用")
        else:
            self.log("未安装 tkinterdnd2，拖拽功能不可用")

    def enable_drag_drop(self):
        if not HAS_DND:
            return

        # 输入框注册拖拽
        self.input_entry.drop_target_register(DND_FILES)
        self.input_entry.dnd_bind("<<Drop>>", self.on_drop_file)

        # 整个窗口也支持拖入
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.on_drop_file)

    def on_drop_file(self, event):
        path = normalize_dropped_file_path(event.data)
        if not path:
            return

        ext = os.path.splitext(path)[1].lower()
        if ext not in SUPPORTED_INPUTS:
            messagebox.showwarning("提示", f"不支持的文件类型: {ext}")
            self.log(f"拖入失败，不支持的文件类型: {path}")
            return

        self.input_path_var.set(path)
        self.update_output_path()
        self.log(f"已拖入文件: {path}")

    def log(self, msg: str):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def clear_log(self):
        self.log_text.delete("1.0", "end")

    def browse_input(self):
        path = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[
                ("字幕/歌词文件", "*.srt *.ass *.ssa *.vtt *.lrc"),
                ("所有文件", "*.*")
            ]
        )
        if path:
            self.input_path_var.set(path)
            self.update_output_path()
            self.log(f"已选择输入文件: {path}")

    def browse_output(self):
        fmt = self.output_format_var.get().lower() or "lrc"
        input_path = self.input_path_var.get().strip()
        initialfile = "output." + fmt

        if input_path:
            initialfile = os.path.basename(strip_extension(input_path)) + "." + fmt

        path = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=f".{fmt}",
            initialfile=initialfile,
            filetypes=[(f"{fmt.upper()} 文件", f"*.{fmt}"), ("所有文件", "*.*")]
        )
        if path:
            self.output_path_var.set(path)
            self.log(f"已设置输出文件: {path}")

    def update_output_path(self, event=None):
        input_path = self.input_path_var.get().strip()
        fmt = self.output_format_var.get().strip().lower()
        if input_path and fmt:
            self.output_path_var.set(f"{strip_extension(input_path)}.{fmt}")

    def run_convert(self):
        input_path = self.input_path_var.get().strip()
        output_format = self.output_format_var.get().strip().lower()
        output_path = self.output_path_var.get().strip()

        if not input_path:
            messagebox.showwarning("提示", "请先选择或拖入输入文件")
            return

        if not os.path.isfile(input_path):
            messagebox.showerror("错误", "输入文件不存在")
            return

        input_ext = os.path.splitext(input_path)[1].lower()
        if input_ext not in SUPPORTED_INPUTS:
            messagebox.showerror("错误", f"不支持的输入格式: {input_ext}")
            return

        if output_format not in SUPPORTED_OUTPUTS:
            messagebox.showerror("错误", f"不支持的输出格式: {output_format}")
            return

        if not output_path:
            output_path = f"{strip_extension(input_path)}.{output_format}"
            self.output_path_var.set(output_path)

        try:
            self.log(f"开始转换: {input_path} -> {output_path}")
            result = convert_file(input_path, output_format, output_path)
            self.log(f"转换完成: {result}")
            messagebox.showinfo("成功", f"转换完成：\n{result}")
        except Exception as e:
            self.log("转换失败:")
            self.log(str(e))
            self.log(traceback.format_exc())
            messagebox.showerror("错误", f"转换失败：\n{e}")


def create_root():
    if HAS_DND:
        return TkinterDnD.Tk()
    return tk.Tk()


def main():
    root = create_root()
    app = ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
