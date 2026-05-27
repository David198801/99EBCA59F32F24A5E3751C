# 检查是否重复，经检查id是唯一的。不同故事会引用同一个文件，链接不同但是文件其实是相同的。
import os

mp3_out_path = r"E:/bestdori/mp3"
mp3_txt_path = mp3_out_path + "/mp3links.txt"

if __name__ == '__main__':
    with open(mp3_txt_path, 'r', encoding='utf-8') as txt:
        l = [x.replace("\n","") for x in txt.readlines()]
        link_count = 0
        filename_dict = {}
        for link in l:
            if link and "/" in link:
                link_count+=1
                filename = link.split("/")[-1]
                links = filename_dict.get(filename)
                if not links:
                    links = []
                    filename_dict[filename] = links
                links.append(link)
        print("链接行数:"+str(link_count))
        print("文件名数量:"+str(len(filename_dict)))
        for filename in filename_dict:
            links = filename_dict[filename]
            if len(links)>1:
                print(links)