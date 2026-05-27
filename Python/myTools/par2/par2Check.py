import os
import subprocess

inPath = r"Y:\f"
outPath = r"F:\p"
par2jPath = "par2j"

# 使用 a+ 模式，防止程序崩溃导致之前的记录丢失
with open("par2Check.txt", "a", encoding="utf8") as txt:
    for root, dirs, files in os.walk(inPath):
        for f in files:
            filePath = os.path.join(root, f)
            
            # 跳过0字节
            if os.path.getsize(filePath) == 0:
                continue
                
            parPath = filePath.replace(inPath, outPath) + ".par2"
            
            if os.path.exists(parPath):
                # 1. 使用列表传参是正确的，避免了Shell注入和空格转义问题
                # 2. 增加 stderr=subprocess.STDOUT 确保捕获完整信息
                comdList = [par2jPath, "v", "/uo", "/d" + root, parPath]
                
                try:
                    p = subprocess.run(comdList, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT, 
                                       check=False)
                    
                    # 尝试用 gbk 解码，不行则用 utf8，再不行则 ignore
                    try:
                        output = p.stdout.decode("gbk")
                    except:
                        output = p.stdout.decode("utf8", "ignore")

                    # 优先判断退出码，再辅助判断字符串
                    if p.returncode == 0 or "All Files Complete" in output:
                        print(f"[OK] {filePath}")
                    else:
                        err_msg = f"[FAILURE] ExitCode:{p.returncode} | Path:{filePath}"
                        print(err_msg)
                        txt.write(err_msg + "\n")
                        # 记录详细错误有助于分析
                        txt.write(f"--- Detail ---\n{output}\n--------------\n")
                
                except Exception as e:
                    print(f"[ERROR] {str(e)}")
                    txt.write(f"[ERROR] {filePath} : {str(e)}\n")
            else:
                print(f"[NO RECORD] {filePath}")
                txt.write(f"[NO RECORD] {filePath}\n")
            
            txt.flush()