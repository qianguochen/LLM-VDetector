import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
from utils import file_handler
from config.enums import VulnerabilityType
from config.settings import VUL_INFO, SOURCE_CODE_INFO


def read_solidity(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def extract_dir(folder_path):
    file_dict = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            absolute_path = os.path.join(root, file)
            if file.endswith(".sol"):
                print(f'文件名：{file}，绝对路径：{absolute_path}')
                file_dict[file] = absolute_path
    absolute_path = Path(folder_path)
    last_folder_name = absolute_path.name
    print(last_folder_name)
    return file_dict, last_folder_name + '.jsonl'


def remove_comments(solidity_code):
    code_without_single_line_comments = re.sub("//.*$", "", solidity_code, flags=re.MULTILINE)
    code_without_multi_line_comments = re.sub("/\*.*?\*/", "", code_without_single_line_comments, flags=re.DOTALL)
    return code_without_multi_line_comments

def task(last_folder_name, file_name, path, vulnerable_info):
    solidity_code = read_solidity(path)
    code_without_multi_line_comments = remove_comments(solidity_code)
    smart_contract_info = {'name': Path(path).name, 'vulnerable_info': vulnerable_info, 'file_path': path,
                           'body': code_without_multi_line_comments}
    file_handler.save_data(last_folder_name, file_name, smart_contract_info)


if __name__ == '__main__':
    thread = 10
    for vulnerable_type in VulnerabilityType:
        file_name = f'DAppScan_{vulnerable_type}.jsonl'
        base_path = SOURCE_CODE_INFO
        file_handler.init_file(base_path, file_name)
        path = f'{VUL_INFO}fix_DAppScan_{vulnerable_type}_vulnerable_info.jsonl'
        data = file_handler.read_data(path)
        for item in data:
            vulnerable_info = {}
            absolute_path = item['file_path']
            vulnerable_info['vul_type'] = item['vul_type']
            vulnerable_info['vul_location'] = item['vul_location']
            vulnerable_info['vulnerable_code'] = item['vulnerable_code']
            with ThreadPoolExecutor(max_workers=thread) as executor:
                executor.submit(task,SOURCE_CODE_INFO, file_name, absolute_path, vulnerable_info)
