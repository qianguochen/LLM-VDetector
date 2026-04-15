import json
import re
import os
from pathlib import Path

from config.enums import VulnerabilityType
from utils import file_handler
from config.enums import PersistencePath

def get_vulnerable_info(path):
    data = file_handler.read_data(path)
    for item in data:
        file_path = item['file_path']
        lines = item['vul_location']
        lines = lines.replace('L', '').replace(' ', '').replace('、', ',').split(',')
        code_list = []
        for item2 in lines:
            source_code = file_handler.read_data(file_path)
            if '-' in item2:
                line = item2.split('-')
                line_code_begin = re.findall(r'\d+', line[0])
                line_code_last = re.findall(r'\d+', line[1])
                try:
                    for i in range(int(line_code_begin[0]), int(line_code_last[0]) + 1):
                        code_list.append(source_code[i - 1].strip())
                except Exception as e:
                    print('-')
                    print(e)
                    print(file_path)
            else:
                try:
                    line_code = int(item2)
                    if 'SWC' in source_code[line_code - 1]:
                        for i in range(line_code - 2, line_code + 2):
                            code_list.append(source_code[i - 1].strip())
                    else:
                        code_list.append(source_code[line_code - 1].strip())
                except Exception as e:
                    print('swc')
                    print(e)
                    print(file_path)

        item['vulnerable_code'] = code_list
        item['file_name'] = os.path.basename(file_path)

        file_handler.save_data(PersistencePath.Vul_Metadata,f'fix_{Path(path).absolute().name}', item)


if __name__ == '__main__':
    for vul in VulnerabilityType:
        get_vulnerable_info(f'{PersistencePath.Vul_Metadata}DAppScan_{vul.value}_vulnerable_info.jsonl')

