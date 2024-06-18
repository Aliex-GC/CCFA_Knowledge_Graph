import os
import re

def process_text_files(input_dir):
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            process_text_file(input_file)

def process_text_file(input_file):
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 找到第一个 'Abstract' 和最后一个 'References' 的位置
    abstract_index = content.find('Abstract')
    references_index = content.rfind('References')

    # 如果找到 'Abstract' 和 'References'
    if abstract_index != -1 and references_index != -1:
        # 截取 'Abstract' 和 'References' 之间的内容
        content = content[abstract_index:references_index]

    # 去除表格和图表相关内容
    content = remove_single_number_lines(content)
    
    # 将处理后的内容写回原文件
    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(content)

def remove_single_number_lines(text):
    # 使用正则表达式匹配单独的数字行和短字符行
    pattern = re.compile(r'^\s*\d+(\.\d+)?\s*$|^\s*[a-zA-Z0-9\s.,%@]{1,10}\s*$', re.MULTILINE)
    text = pattern.sub('', text)
    # 匹配特定格式的行
    number_line_pattern = re.compile(r'^\s*\d+(\.\d+)?\s*$', re.MULTILINE)
    short_line_pattern = re.compile(r'^\s*[a-zA-Z\s.,%@]{1,10}\s*$', re.MULTILINE)
    multi_number_line_pattern = re.compile(r'^\s*(\d+\.\d+\s*){2,}\s*$', re.MULTILINE)
    short_line_any_pattern = re.compile(r'^.{1,10}$', re.MULTILINE)
    # 删除匹配的行
    text = number_line_pattern.sub('', text)
    text = short_line_pattern.sub('', text)
    text = multi_number_line_pattern.sub('', text)
    text = short_line_any_pattern.sub('', text)
    # 移除多余的空行
    text = re.sub(r'\n+', '\n', text)
    
    return text

def renumber_txt_files(input_dir, start_number):
    # 获取目录下所有的txt文件
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    # 排序文件以确保重命名的顺序一致
    txt_files.sort()
    
    # 设定初始编号
    current_number = start_number
    
    for file in txt_files:
        # 构造旧文件路径和新文件路径
        old_path = os.path.join(input_dir, file)
        new_filename = f"{current_number}.txt"
        new_path = os.path.join(input_dir, new_filename)
        
        # 重命名文件
        os.rename(old_path, new_path)
        
        # 更新编号
        current_number += 1

    print("Renumbering completed.")

# 使用示例，处理目录中的所有文件
input_dir = './data_input/cureus/'
start_number = 46

# 调用函数进行文件重命名
renumber_txt_files(input_dir, start_number)
process_text_files(input_dir)
