import os
import sys
from pathlib import Path
import json
from utils import file_handler
from config import enums
from config.enums import PersistencePath

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
                        file_handler.save_data(PersistencePath.Vul_Metadata,file_name, vul_info)


def divide_vulnerable(path):
    data_list = file_handler.read_data(path)
    for vul_type in enums.VulnerabilityType:
        for vul_data in data_list:

            vulnerable_type = vul_data['vul_type']
            if vul_type.replace('_', ' ') in vulnerable_type:
                file_handler.save_data(PersistencePath.Vul_Metadata,
                    'DAppScan_' + vul_type.replace(' ', '_') + '_vulnerable_info.jsonl',
                    vul_data)


def divide_vulnerable_contract(path, type):
    data = file_handler.read_data(path)
    for item in data:
        vul_data = json.loads(item)
        file_path = vul_data['file_path']
        with open(file_path, 'r', encoding='utf-8') as f2:
            try:
                contract_code = f2.read()
            except Exception as e:
                print(file_path)
                print(e)
        file_name = file_path.split('/')[-1]
        save_path = 'DAppScan_Contracts/' + type + '/' + file_name
        if not os.path.exists('DAppScan_Contracts/' + type):
            os.mkdir('DAppScan_Contracts/' + type)
        with open(save_path, 'w', encoding='utf-8') as f3:
            try:
                f3.write(contract_code)
            except Exception as e:
                print(file_path)
                print(e)


if __name__ == '__main__':
    data_path = PersistencePath.Vul_Source_Base
    save_file_name = 'DAppScan_vulnerable_info.jsonl'
    extract_dir(data_path, save_file_name)
    divide_vulnerable(PersistencePath.Vul_Metadata+save_file_name)