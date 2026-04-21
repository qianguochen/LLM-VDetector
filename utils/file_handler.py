import os
import json
import re
import threading
from pathlib import Path


def init_file(path, file_name):
    """
        初始化文件：如果文件存在则清空内容，不存在则创建空文件

        Args:
            path: 目录路径
            file_name: 文件名

        Returns:
            str: 文件完整路径
        """
    # 确保目录存在
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, file_name)

    # "w" 模式：文件存在则清空，不存在则创建
    with open(file_path, "w") as f:
        pass  # 清空或创建空文件


def save_data(base_path, file_name, data):
    if not os.path.exists(base_path + file_name):
        with open(base_path + file_name, "w") as f:
            pass
    with open(base_path + file_name, 'a', encoding='utf-8') as f:
        try:
            if isinstance(data, list) and len(data) >= 1:
                for item in data:
                    write_line = json.dumps(item)
                    f.write(write_line + '\n')
            else:
                write_line = json.dumps(data)
                f.write(write_line + '\n')
        except Exception as e:
            print(e)

def read_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if path.endswith('.json'):
                data = json.load(f)
                return data
            elif path.endswith('.jsonl'):
                data = []
                for item in f.readlines():
                    data.append(json.loads(item))
                return data
            elif path.endswith('.sol'):
                return f.readlines()
            return None
    except FileNotFoundError:
        return {} if path.endswith('.json') else []
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误 ({path}): {e}")
        return [] if path.endswith('.jsonl') else []
    except Exception as e:
        print(f"读取文件错误 ({path}): {e}")
        return '' if path.endswith('.sol') else []


def extract_dir(folder_path, file_suffix):
    file_info_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            absolute_path = os.path.join(root, file)
            file_info = {}
            if file.endswith(file_suffix):
                # print(f'文件名：{file}，绝对路径：{absolute_path}')
                file_info[file] = absolute_path
                file_info_list.append(file_info)
    absolute_path = Path(folder_path)
    last_folder_name = absolute_path.name
    return file_info_list, last_folder_name + '.jsonl'


def get_file_name(file_path):
    path = Path(file_path)
    return path.name


def has_letter(s):
    return any(c.isalpha() for c in s)


def get_code_snippet_by_line(line_info, source_code):
    code_list = []
    if '-' in line_info:
        line = line_info.split('-')
        line_code_begin = re.findall(r'\d+', line[0])
        line_code_last = re.findall(r'\d+', line[1])
        try:
            for i in range(int(line_code_begin[0]), int(line_code_last[0]) + 1):
                code_list.append(source_code[i - 1].strip())
        except Exception as e:
            print('-')
            print(code_list)
            print(e)

    else:
        try:
            if has_letter(line_info):
                code_list = source_code
            else:
                line_code = int(line_info)
                if 'SWC' in source_code[line_code - 1]:
                    for i in range(line_code - 2, line_code + 2):
                        code_list.append(source_code[i - 1].strip())
                else:
                    code_list.append(source_code[line_code - 1].strip())
        except Exception as e:
            print('swc')
            print(code_list)
            print(e)
    return code_list


def has_duplicate_lines(input_file, output_file):
    """
       移除 JSONL 文件中的重复行（基于字符串对比）

       Args:
           input_file: 输入文件路径
           output_file: 输出文件路径
       """
    seen_lines = set()
    duplicates_count = 0

    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        for line in infile:
            # 去除行尾换行符进行对比
            line_content = line.rstrip('\n')

            # 跳过空行
            if not line_content:
                continue

            # 检查是否已经见过这行
            if line_content not in seen_lines:
                seen_lines.add(line_content)
                # outfile.write(line)  # 写入原始行（包含换行符）
            else:
                duplicates_count += 1

    print(f"处理完成！")
    print(f"发现重复行: {duplicates_count}")
    print(f"保留唯一行: {len(seen_lines)}")
