import os
import json

# 获取脚本所在的当前目录
current_directory = os.path.dirname(os.path.realpath(__file__))

# 处理.mtn文件，删除字符串"PARAM_MOUTH_OPEN_Y=0"
def remove_string_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容
            content = file.read()
        
        # 删除所有的"PARAM_MOUTH_OPEN_Y=0"
        content = content.replace('PARAM_MOUTH_OPEN_Y=0', '').replace('PARAM_MOUTH_OPEN_Y=1', '')
        
        # 将修改后的内容写回原文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Successfully modified: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# 处理.exp.json文件，删除params中id为"PARAM_MOUTH_OPEN_Y"的元素
def remove_param_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取JSON文件内容
            data = json.load(file)
        
         # 获取params属性，删除id为"PARAM_MOUTH_OPEN_Y"和"PARAM_EYE_L_OPEN"且val大于等于1的元素
        if 'params' in data:
            data['params'] = [
                param for param in data['params']
                if not (
                    (param.get('id') == 'PARAM_MOUTH_OPEN_Y') or
                    (param.get('id') == 'PARAM_EYE_L_OPEN' and param.get('val', 0) >= 1) or
                    (param.get('id') == 'PARAM_EYE_R_OPEN' and param.get('val', 0) >= 1)
                )
            ]
        
        # 将修改后的数据写回原文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print(f"Successfully modified: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        
idle_content = """# Live2D Animator Motion Data
$fps=30

$fadein=1000

$fadeout=1000

PARAM_EYE_L_OPEN=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.74,0.26,0,0,0,0,0,0.24,0.64,0.91,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.74,0.26,0,0,0,0.24,0.64,0.91,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1

PARAM_EYE_L_SMILE=0

PARAM_EYE_R_OPEN=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.74,0.26,0,0,0,0,0,0.24,0.64,0.91,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.74,0.26,0,0,0,0.24,0.64,0.91,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1

PARAM_EYE_R_SMILE=0""" 
        
def deal_model_json(file_path):
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 获取 motions 属性中的任意一个子属性（假设我们知道它是一个字典）
    motions = data.get('motions', {})
    
    mtn_path = None
    # 获取任意一个子属性的第一个元素，并获取 "file" 属性
    for key, value in motions.items():
        if isinstance(value, list) and len(value) > 0:
            # 这里获取第一个元素的 "file" 属性
            mtn_path = value[0].get('file', None)
    if mtn_path:
        mtn_rela_path = os.path.dirname(mtn_path)+"/"+"idle.mtn"
        mtn_abs_path = os.path.dirname(file_path)+"/"+mtn_rela_path
        with open(mtn_abs_path, 'w', encoding='utf-8') as output_file:
            output_file.write(idle_content)
            
        # 添加新的元素到 motions
        new_motion = {"idle": [{"file": mtn_rela_path}]}
        motions.update(new_motion)  # 将新的 motion 元素添加到 motions

        # 将修改后的数据写回原始 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
            print(f"已将修改后的 JSON 写回到文件: {file_path}")

# 递归遍历目录下所有文件
def traverse_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 处理以.mtn结尾的文件
            if file.endswith('.mtn'):
                remove_string_from_file(file_path)
            # 处理以.exp.json结尾的文件
            elif file.endswith('.exp.json'):
                remove_param_from_json(file_path)
            # 处理model.json
            elif file == "model.json":
                deal_model_json(file_path)

# 开始遍历从脚本所在目录开始
traverse_directory(current_directory)