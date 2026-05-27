import fitz  # PyMuPDF
from PIL import Image
import io
import os

def extract_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pdf = fitz.open(pdf_path)
    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf.extract_image(xref)
            image_bytes = base_image["image"]
            # 保存为PNG（无损格式）
            with open(f"{output_folder}/page{page_num+1:04d}_img{img_index+1:04d}.png", "wb") as f:
                f.write(image_bytes)
                
# main函数，获取脚本当前路径，递归遍历当前路径，获取pdf文件，然后执行extract_images，输出路径为pdf的路径去掉后缀名
def main():
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 递归遍历当前目录及所有子目录
    for root, dirs, files in os.walk(script_dir):
        for file in files:
            # 检查是否为PDF文件
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                
                # 创建输出文件夹路径（移除文件扩展名）
                output_folder = os.path.splitext(pdf_path)[0]
                
                print(f"处理文件: {pdf_path}")
                print(f"输出到: {output_folder}")
                
                # 提取图像
                extract_images(pdf_path, output_folder)
                
    print("所有PDF文件处理完成！")

if __name__ == "__main__":
    main()