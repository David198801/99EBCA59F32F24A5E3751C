import os
#检查前20个字节是0的异常文件，忽略ISO
def check_corrupted_files(directory_path, output_txt_path):
    # 定义20个连续的0字节，用于普通文件
    target_pattern = b'\x00' * 20
    
    # 预先定义一个8MB的全0字节块，用于高效对比大型iso文件
    CHUNK_SIZE = 8 * 1024 * 1024
    ZERO_CHUNK = b'\x00' * CHUNK_SIZE
    
    print("正在统计文件总数，请稍候...")
    total_files = 0
    # 第一次遍历：仅用于统计文件总数
    for root, dirs, files in os.walk(directory_path):
        total_files += len(files)
        
    if total_files == 0:
        print("指定目录中没有找到任何文件。")
        return 0
        
    print(f"统计完毕，共发现 {total_files} 个文件。开始深度扫描...\n")

    corrupted_count = 0
    processed_count = 0

    # 打开TXT文件用于记录异常文件路径 (使用utf-8编码防止特殊路径字符报错)
    with open(output_txt_path, 'w', encoding='utf-8') as out_file:
        out_file.write(f"以下是目录 {directory_path} 中被检测为疑似损坏的文件：\n")
        out_file.write("-" * 50 + "\n")
        
        # 第二次遍历：执行实质性的文件读取和检测
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                processed_count += 1
                file_path = os.path.join(root, file)
                
                # 获取文件扩展名（转小写以便统一判断）
                file_ext = os.path.splitext(file)[1].lower()
                
                # 进度前缀格式：[已处理/总数]
                progress_prefix = f"[{processed_count}/{total_files}]"
                is_corrupted = False
                
                try:
                    if file_ext == '.iso':
                        # ==========================================
                        # 逻辑1: ISO文件，检查是否整个文件全部为0
                        # ==========================================
                        file_size = os.path.getsize(file_path)
                        
                        if file_size > 0:
                            is_corrupted = True # 先假设它全是0
                            with open(file_path, 'rb') as f:
                                while True:
                                    chunk = f.read(CHUNK_SIZE)
                                    if not chunk:
                                        break # 读到文件末尾
                                    
                                    # 将读到的块与标准0块比对（切片处理最后一次读取不足CHUNK_SIZE的情况）
                                    if chunk != ZERO_CHUNK[:len(chunk)]:
                                        is_corrupted = False # 发现非0数据，文件正常
                                        break
                        else:
                            # 如果文件大小为0字节，则它不存在"全部为0"的实质内容，视作不满足损坏条件
                            is_corrupted = False
                            
                    else:
                        # ==========================================
                        # 逻辑2: 其余文件，检查前20个字节是否为0
                        # ==========================================
                        with open(file_path, 'rb') as f:
                            header_data = f.read(20)
                            # 如果文件大于等于20字节且前20个字节全为0
                            if len(header_data) == 20 and header_data == target_pattern:
                                is_corrupted = True
                    
                    # === 最终判断输出 ===
                    if is_corrupted:
                        print(f"{progress_prefix} [警告] 发现疑似损坏: {file_path}")
                        corrupted_count += 1
                        # 写入到TXT记录文件中
                        out_file.write(file_path + "\n")
                        out_file.flush()
                    else:
                        print(f"{progress_prefix} [正常] {file_path}")
                            
                except PermissionError:
                    print(f"{progress_prefix} [跳过] 权限拒绝: {file_path}")
                except FileNotFoundError:
                    print(f"{progress_prefix} [跳过] 文件已不存在(可能刚被删除): {file_path}")
                except Exception as e:
                    print(f"{progress_prefix} [错误] 读取异常 {file_path}: {e}")

    return corrupted_count

if __name__ == '__main__':
    # ==========================================
    # 在这里硬编码你的目标目录路径 和 结果输出TXT文件路径
    # ==========================================
    TARGET_DIRECTORY = r"Z:\f" 
    OUTPUT_TXT = "corrupted_files_log.txt"  # 结果将保存在脚本所在目录
    
    if os.path.isdir(TARGET_DIRECTORY):
        print(f"目标目录: {TARGET_DIRECTORY}")
        print(f"异常文件记录将保存至: {os.path.abspath(OUTPUT_TXT)}\n")
        
        total_corrupted = check_corrupted_files(TARGET_DIRECTORY, OUTPUT_TXT)
        
        print("-" * 50)
        print(f"扫描完成！")
        print(f"共发现 {total_corrupted} 个疑似损坏的文件。")
        if total_corrupted > 0:
            print(f"详细的损坏文件列表已保存至: {os.path.abspath(OUTPUT_TXT)}")
        else:
            print("未发现损坏文件，目录健康。")
    else:
        print(f"错误: 目录路径不存在 -> {TARGET_DIRECTORY}")