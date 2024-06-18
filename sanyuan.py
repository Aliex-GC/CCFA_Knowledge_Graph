import os
import re

def replace_separator_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace '|' with ' '
    new_content = content.replace('|', ' ')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def process_directory(directory_path):
    pattern = re.compile(r'.*_graph$')
    for filename in os.listdir(directory_path):
        if pattern.match(filename):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                replace_separator_in_file(file_path)
                print(f'Processed file: {file_path}')

# Specify the directory containing the files
directory_path =  './data_output/cureus/'

# Process all files in the specified directory
process_directory(directory_path)
