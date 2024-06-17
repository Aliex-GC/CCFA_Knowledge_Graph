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
    content = remove_tables_and_figures(content)
    
    # 将处理后的内容写回原文件
    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(content)

def remove_tables_and_figures(content):
    # 匹配表格和图表的正则表达式
    table_pattern = re.compile(r'Table \d+.*?\n(?:.*?\n)*?\n')
    figure_pattern = re.compile(r'Figure \d+.*?\n(?:.*?\n)*?\n')
    
    # 去除表格和图表
    content = re.sub(table_pattern, '', content)
    content = re.sub(figure_pattern, '', content)
    
    return content

# 使用示例，处理目录中的所有文件
input_dir = './data_input/cureus/'
process_text_files(input_dir)
