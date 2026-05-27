import os
from pypdf import PdfReader

# =========================
# 硬编码目录
# =========================
ROOT_DIR = r"E:\BaiduNetdiskDownload\temp\儿童文学1963-2023"


def get_pdf_files(root_dir):
    """递归获取所有 PDF 文件路径"""
    pdf_files = []
    for current_root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(current_root, file))
    return pdf_files


def get_pdf_page_count(pdf_path):
    """获取单个 PDF 页数"""
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception as e:
        print(f"\n读取失败: {pdf_path}，错误: {e}")
        return None


def split_into_3_intervals(page_counts):
    """根据最小页数和最大页数自动分成 3 个区间"""
    min_pages = min(page_counts)
    max_pages = max(page_counts)

    if min_pages == max_pages:
        return [((min_pages, max_pages), len(page_counts))]

    total_range = max_pages - min_pages + 1
    step = total_range / 3

    b1 = min_pages
    b2 = int(min_pages + step)
    b3 = int(min_pages + 2 * step)
    b4 = max_pages

    intervals = [
        (b1, b2),
        (b2 + 1, b3),
        (b3 + 1, b4),
    ]

    result = []
    for start, end in intervals:
        count = sum(1 for p in page_counts if start <= p <= end)
        result.append(((start, end), count))
    return result


def main():
    print(f"正在扫描目录: {ROOT_DIR}")
    pdf_files = get_pdf_files(ROOT_DIR)

    if not pdf_files:
        print("未找到任何 PDF 文件。")
        return

    total = len(pdf_files)
    print(f"共找到 {total} 个 PDF 文件，开始统计页数...\n")

    page_data = []
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\r进度: [{i}/{total}] {os.path.basename(pdf_file)}", end="", flush=True)
        pages = get_pdf_page_count(pdf_file)
        if pages is not None:
            page_data.append((pdf_file, pages))

    print()  # 换行

    if not page_data:
        print("没有成功读取任何 PDF 页数。")
        return

    page_counts = [pages for _, pages in page_data]

    total_files = len(page_counts)
    max_pages = max(page_counts)
    min_pages = min(page_counts)
    avg_pages = sum(page_counts) / total_files

    print("=" * 50)
    print(f"扫描目录: {ROOT_DIR}")
    print(f"成功统计文件数: {total_files}")
    print(f"最大页数: {max_pages}")
    print(f"最小页数: {min_pages}")
    print(f"平均页数: {avg_pages:.2f}")
    print("=" * 50)

    print("三个自动区间统计：")
    for (start, end), count in split_into_3_intervals(page_counts):
        print(f"{start} - {end} 页: {count} 个文件")

    print("=" * 50)


if __name__ == "__main__":
    main()