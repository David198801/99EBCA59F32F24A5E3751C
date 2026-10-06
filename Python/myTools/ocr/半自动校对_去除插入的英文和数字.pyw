import re
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QStatusBar,
)


class OCRTextCleaner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OCR 文本人工校对工具")
        self.resize(1000, 700)
        self.setAcceptDrops(True)

        self.file_path = None
        self.matches = []
        self.current_match_index = -1

        # 逻辑保持不变：连续 3~20 位非中文字符都高亮（排除空白）
        self.pattern = re.compile(r"[^\u4e00-\u9fff\s]{3,20}")

        self.text = None
        self.rule_label = None
        self.drop_hint = None
        self.status_bar = None

        self.create_widgets()

    def create_widgets(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(6)

        btn_open = QPushButton("打开文件")
        btn_open.clicked.connect(self.open_file)
        toolbar_layout.addWidget(btn_open)

        btn_scan = QPushButton("重新扫描")
        btn_scan.clicked.connect(self.scan_text)
        toolbar_layout.addWidget(btn_scan)

        btn_prev = QPushButton("上一个")
        btn_prev.clicked.connect(self.prev_match)
        toolbar_layout.addWidget(btn_prev)

        btn_next = QPushButton("下一个")
        btn_next.clicked.connect(self.next_match)
        toolbar_layout.addWidget(btn_next)

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.save_file)
        toolbar_layout.addWidget(btn_save)

        btn_save_as = QPushButton("另存为")
        btn_save_as.clicked.connect(self.save_as_file)
        toolbar_layout.addWidget(btn_save_as)

        btn_undo = QPushButton("撤销")
        btn_undo.clicked.connect(self.undo)
        toolbar_layout.addWidget(btn_undo)

        btn_redo = QPushButton("重做")
        btn_redo.clicked.connect(self.redo)
        toolbar_layout.addWidget(btn_redo)

        rule_text = "规则：高亮连续 3~20 位非中文字符；支持拖拽载入"
        self.rule_label = QLabel(rule_text)
        self.rule_label.setStyleSheet("color: gray;")
        toolbar_layout.addWidget(self.rule_label)

        toolbar_layout.addStretch()
        main_layout.addLayout(toolbar_layout)

        self.text = QTextEdit()
        self.text.setAcceptRichText(False)
        self.text.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 12pt;")
        main_layout.addWidget(self.text)

        self.drop_hint = QLabel("可将 .txt 文件拖到窗口中打开")
        self.drop_hint.setStyleSheet("color: gray;")
        self.drop_hint.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.drop_hint)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("未打开文件")

        # 可选：菜单快捷键
        self.create_actions()

    def create_actions(self):
        action_open = QAction("打开文件", self)
        action_open.triggered.connect(self.open_file)
        action_open.setShortcut("Ctrl+O")
        self.addAction(action_open)

        action_save = QAction("保存", self)
        action_save.triggered.connect(self.save_file)
        action_save.setShortcut("Ctrl+S")
        self.addAction(action_save)

        action_undo = QAction("撤销", self)
        action_undo.triggered.connect(self.undo)
        action_undo.setShortcut("Ctrl+Z")
        self.addAction(action_undo)

        action_redo = QAction("重做", self)
        action_redo.triggered.connect(self.redo)
        action_redo.setShortcut("Ctrl+Y")
        self.addAction(action_redo)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                path = urls[0].toLocalFile()
                if path.lower().endswith(".txt"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        path = urls[0].toLocalFile()
        if not path.lower().endswith(".txt"):
            QMessageBox.warning(self, "提示", "只支持拖拽载入 .txt 文件。")
            return

        self.load_file(path)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "打开文件",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )
        if path:
            self.load_file(path)

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            QMessageBox.critical(self, "错误", "文件不是有效的 UTF-8 编码。")
            return
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开文件失败：\n{e}")
            return

        self.text.setPlainText(content)
        self.file_path = path
        self.scan_text()
        self.status_bar.showMessage(f"已打开：{path}")

    def save_file(self):
        if not self.file_path:
            self.save_as_file()
            return

        try:
            content = self.text.toPlainText().rstrip("\n")
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.status_bar.showMessage(f"已保存：{self.file_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败：\n{e}")

    def save_as_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "另存为",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )
        if not path:
            return

        try:
            content = self.text.toPlainText().rstrip("\n")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.file_path = path
            self.status_bar.showMessage(f"已另存为：{path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"另存失败：\n{e}")

    def scan_text(self):
        content = self.text.toPlainText()

        self.clear_highlights()
        self.matches = []
        self.current_match_index = -1

        for match in self.pattern.finditer(content):
            start_pos = match.start()
            end_pos = match.end()
            self.add_highlight(start_pos, end_pos, current=False)
            self.matches.append((start_pos, end_pos))

        if self.matches:
            self.current_match_index = 0
            self.highlight_current_match()
            self.status_bar.showMessage(f"扫描完成：发现 {len(self.matches)} 处可疑片段")
        else:
            self.status_bar.showMessage("扫描完成：未发现可疑片段")

    def clear_highlights(self):
        cursor = self.text.textCursor()
        cursor.beginEditBlock()

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("transparent"))
        fmt.setForeground(QColor("black"))

        cursor.select(QTextCursor.Document)
        cursor.mergeCharFormat(fmt)

        cursor.endEditBlock()

    def add_highlight(self, start, end, current=False):
        cursor = self.text.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)

        fmt = QTextCharFormat()
        if current:
            fmt.setBackground(QColor("orange"))
            fmt.setForeground(QColor("black"))
        else:
            fmt.setBackground(QColor("yellow"))
            fmt.setForeground(QColor("red"))

        cursor.mergeCharFormat(fmt)

    def highlight_current_match(self):
        # 先重绘全部普通高亮
        self.clear_highlights()
        for start, end in self.matches:
            self.add_highlight(start, end, current=False)

        if 0 <= self.current_match_index < len(self.matches):
            start, end = self.matches[self.current_match_index]
            self.add_highlight(start, end, current=True)

            cursor = self.text.textCursor()
            cursor.setPosition(start)
            self.text.setTextCursor(cursor)
            self.text.ensureCursorVisible()
            self.text.setFocus()

            self.status_bar.showMessage(
                f"第 {self.current_match_index + 1} / {len(self.matches)} 处可疑片段"
            )

    def next_match(self):
        if not self.matches:
            return
        self.current_match_index = (self.current_match_index + 1) % len(self.matches)
        self.highlight_current_match()

    def prev_match(self):
        if not self.matches:
            return
        self.current_match_index = (self.current_match_index - 1) % len(self.matches)
        self.highlight_current_match()

    def undo(self):
        self.text.undo()

    def redo(self):
        self.text.redo()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRTextCleaner()
    window.show()
    sys.exit(app.exec())