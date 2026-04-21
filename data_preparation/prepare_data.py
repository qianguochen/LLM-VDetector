import os
import sys
from pathlib import Path
from utils import file_handler
from config.enums import VulnerabilityType
from config.settings import VUL_INFO,VUL_SOURCE_BASE

def extract_dir(folder_path, file_name):
    folder_path = Path(folder_path).resolve()
    for file_path in folder_path.rglob("*.sol"):  # 递归查找所有 .sol 文件
        absolute_path = str(file_path.absolute())
        if sys.platform == 'win32' and len(absolute_path) >= 260:
            if not absolute_path.startswith('\\\\?\\'):
                absolute_path = '\\\\?\\' + os.path.abspath(absolute_path)
                print(f"Using long path prefix: {absolute_path[:100]}...")
        try:
            source_code = file_handler.read_data(absolute_path)
        except Exception as e:
            print(f"Error reading {absolute_path}: {e}")
            print(len(absolute_path))
        else:
            count_line = 0
            if source_code is not None:
                for item in source_code:
                    count_line += 1
                    vul_info = {}
                    if 'SWC-' in item:
                        vul_info['file_path'] = absolute_path
                        vul_info['vul_type'] = item.split(':')[0].replace('//', '').strip()
                        try:
                            vul_info['vul_location'] = item.split(':')[1].strip()
                        except IndexError:
                            vul_info['vul_location'] = f"L{count_line + 1}"
                            count_line = 0
                        file_handler.save_data(VUL_INFO, file_name, vul_info)


def divide_vulnerable(path):
    data_list = file_handler.read_data(path)
    for vul_type in VulnerabilityType:
        for vul_data in data_list:
            vulnerable_type = vul_data['vul_type']
            if vul_type.replace('_', ' ') in vulnerable_type:
                file_handler.save_data(VUL_INFO,
                                       'DAppScan_' + vul_type.replace(' ', '_') + '_vulnerable_info.jsonl',
                                       vul_data)


def get_vulnerable_info(path):
    data = file_handler.read_data(path)
    for item in data:
        file_path = item['file_path']
        lines = item['vul_location']
        lines = lines.replace('L', '').replace(' ', '').replace('、', ',').split(',')
        for item2 in lines:
            source_code = file_handler.read_data(file_path)
            code_list = file_handler.get_code_snippet_by_line(item2, source_code)
            item['vulnerable_code'] = code_list
            item['file_name'] = os.path.basename(file_path)
            file_handler.save_data(VUL_INFO, f'fix_{Path(path).absolute().name}', item)


# 源码实验数据准备
if __name__ == '__main__':
    # 提取漏洞基础信息
    data_path = VUL_SOURCE_BASE
    save_file_name = 'DAppScan_vulnerable_info.jsonl'
    extract_dir(data_path, save_file_name)
    # 根据漏洞类型切分
    divide_vulnerable(VUL_INFO + save_file_name)
    # 补充漏洞位置源码信息
    for vul in VulnerabilityType:
        get_vulnerable_info(f'{VUL_INFO}DAppScan_{vul.value}_vulnerable_info.jsonl')
