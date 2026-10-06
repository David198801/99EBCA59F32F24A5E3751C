import re
from pathlib import Path
from markdown_it import MarkdownIt

# =========================
# 硬编码配置
# =========================
INPUT_ROOT = Path(r"D:\360极速浏览器X下载\kl3300\workplace\output\02 一群人的世界").resolve()
OUTPUT_TXT = Path(r"D:\360极速浏览器X下载\kl3300\一群人的世界.txt").resolve()

# 是否忽略 md 文件内部标题
IGNORE_MD_HEADINGS = True

# 是否忽略除普通文本外的其他 Markdown 内容
IGNORE_INLINE_CODE = True
IGNORE_CODE_BLOCKS = True
IGNORE_IMAGES = True
IGNORE_LINK_TEXT = True
IGNORE_LISTS = True
IGNORE_BLOCKQUOTES = True

# 如果某一行只包含以下字符串中的某一个 + 空白字符，则忽略该行
IGNORED_LINE_STRINGS = [
    "上一章",
    "下一章",
]

SEPARATOR = "=" * 40

md_parser = MarkdownIt()

# 预编译忽略行正则
IGNORED_LINE_PATTERNS = [
    re.compile(rf"^\s*{re.escape(text)}\s*$")
    for text in IGNORED_LINE_STRINGS
]


def get_title(md_path: Path) -> str:
    """
    使用 md 文件所在目录的上一层目录名作为标题
    例如: /a/b/c/file.md -> 标题是 b
    """
    parent_dir = md_path.parent
    upper_dir = parent_dir.parent
    return upper_dir.name if upper_dir.name else parent_dir.name


def collect_md_files(root: Path) -> list[Path]:
    """
    递归查找所有 .md 文件，并按绝对路径字符串顺序排序
    """
    md_files = [p.resolve() for p in root.rglob("*.md") if p.is_file()]
    md_files.sort(key=lambda p: str(p))
    return md_files


def should_ignore_line(line: str) -> bool:
    """
    如果一行只包含忽略列表中的某个字符串和空白字符，则返回 True。
    """
    return any(pattern.fullmatch(line) for pattern in IGNORED_LINE_PATTERNS)


def extract_text_from_markdown(markdown_text: str) -> str:
    """
    使用 markdown-it-py 解析 Markdown，只提取需要保留的文本内容。
    """
    tokens = md_parser.parse(markdown_text)
    parts = []

    heading_level = 0
    list_level = 0
    blockquote_level = 0
    link_level = 0

    def should_ignore_current_text() -> bool:
        if IGNORE_MD_HEADINGS and heading_level > 0:
            return True
        if IGNORE_LISTS and list_level > 0:
            return True
        if IGNORE_BLOCKQUOTES and blockquote_level > 0:
            return True
        if IGNORE_LINK_TEXT and link_level > 0:
            return True
        return False

    def walk_tokens(token_list):
        nonlocal heading_level, list_level, blockquote_level, link_level

        for token in token_list:
            token_type = token.type

            if token_type == "heading_open":
                heading_level += 1
                continue
            if token_type == "heading_close":
                heading_level = max(heading_level - 1, 0)
                parts.append("\n")
                continue

            if token_type in ("bullet_list_open", "ordered_list_open"):
                list_level += 1
                continue
            if token_type in ("bullet_list_close", "ordered_list_close"):
                list_level = max(list_level - 1, 0)
                parts.append("\n")
                continue

            if token_type == "blockquote_open":
                blockquote_level += 1
                continue
            if token_type == "blockquote_close":
                blockquote_level = max(blockquote_level - 1, 0)
                parts.append("\n")
                continue

            if token_type == "link_open":
                link_level += 1
                continue
            if token_type == "link_close":
                link_level = max(link_level - 1, 0)
                continue

            if token_type == "inline" and token.children:
                walk_tokens(token.children)
                continue

            if token_type == "text":
                if not should_ignore_current_text():
                    parts.append(token.content)
                continue

            if token_type == "code_inline":
                if not IGNORE_INLINE_CODE and not should_ignore_current_text():
                    parts.append(token.content)
                continue

            if token_type in ("code_block", "fence"):
                if not IGNORE_CODE_BLOCKS:
                    content = token.content.rstrip()
                    if content:
                        parts.append(content)
                        parts.append("\n")
                continue

            if token_type == "image":
                if not IGNORE_IMAGES and not should_ignore_current_text() and token.content:
                    parts.append(token.content)
                continue

            if token_type in ("softbreak", "hardbreak"):
                if not should_ignore_current_text():
                    parts.append("\n")
                continue

            if token_type in ("paragraph_close", "list_item_close"):
                parts.append("\n")
                continue

    walk_tokens(tokens)

    raw_lines = "".join(parts).splitlines()
    cleaned_lines = [line.rstrip() for line in raw_lines]

    final_lines = []
    prev_blank = False
    for line in cleaned_lines:
        if should_ignore_line(line):
            continue

        is_blank = line.strip() == ""
        if is_blank:
            if not prev_blank:
                final_lines.append("")
            prev_blank = True
        else:
            final_lines.append(line)
            prev_blank = False

    return "\n".join(final_lines).strip()


def merge_md_to_txt(input_root: Path, output_txt: Path) -> None:
    md_files = collect_md_files(input_root)
    output_txt.parent.mkdir(parents=True, exist_ok=True)

    with output_txt.open("w", encoding="utf-8") as out_file:
        for md_file in md_files:
            title = get_title(md_file)
            markdown_text = md_file.read_text(encoding="utf-8")
            plain_text = extract_text_from_markdown(markdown_text)

            out_file.write(f"{title}\n")

            if plain_text:
                for line in plain_text.splitlines():
                    out_file.write(f"    {line}\n")

            out_file.write("\n")
            out_file.write(f"{SEPARATOR}\n")


if __name__ == "__main__":
    merge_md_to_txt(INPUT_ROOT, OUTPUT_TXT)
    print(f"合并完成: {OUTPUT_TXT}")