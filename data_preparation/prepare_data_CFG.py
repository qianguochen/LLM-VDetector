import json
from pathlib import Path
from utils import file_handler
import os
from typing import Dict, Any
import tiktoken
from config.enums import PersistencePath
from config.enums import VulnerabilityType
from fileter_source_code import remove_comments,read_solidity

def extract_dir_cfg(folder_path, file_name):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            absolute_path = os.path.join(root, file)
            if file.endswith(".json"):
                # print(f'文件名：{file}，绝对路径：{absolute_path}')
                if len(absolute_path) > 240:
                    absolute_path = fr"\\?\{absolute_path}"
                    print(absolute_path)
                with open(absolute_path, 'r') as f:
                    data = f.read()
                    data = json.loads(data)
                    file_handler.save_data(PersistencePath.vul_cfg_info, file_name, data)


# 根据漏洞类型分类
def divide_vulnerable(path):
    data_list = file_handler.read_data(path)
    for vul_type in VulnerabilityType:
        for vul_data in data_list:
            for item in vul_data['SWCs']:
                vul_line = {}
                vulnerable_type = item['category']
                if vul_type.replace('_', ' ') in vulnerable_type:
                    vul_line['node_name'] = vul_data['node name']
                    vul_line['file_path'] = item['sourcePath']
                    vul_line['vul_type'] = vulnerable_type
                    vul_line['vul_location'] = item['lines']
                    vul_line['function'] = item['function']
                    file_handler.save_data(PersistencePath.vul_cfg_info,
                                           'DAppScan_' + vul_type.replace(' ', '_') + '_vulnerable_info_cfg.jsonl',
                                           vul_line)


# 搜集bytecode文件夹编译好的json文件路径信息
def collect_ast_data_from_bytecode(folder_path, file_suffix):
    data = file_handler.extract_dir(folder_path, file_suffix)
    folder_name = data[1]
    for item in data[0]:
        file_handler.save_data(PersistencePath.vul_cfg_info, 'DAppSCAN_' + folder_name, item)


# 补充漏洞信息的源码用于判断 控制流图
def get_vulnerable_info_cfg(path):
    data = file_handler.read_data(path)
    for item in data:
        file_path = item['file_path'].replace('rce/contracts/', '', 1)
        file_path = Path(fr"{PersistencePath.Vul_Source_Base}{file_path}")
        lines = item['vul_location']
        lines = lines.replace('L', '').replace(' ', '').split(',')
        for item2 in lines:
            print(item2)
            source_code = file_handler.read_data(str(file_path.absolute()))
            code_list = file_handler.get_code_snippet_by_line(item2, source_code)
            item['file_path'] = str(file_path.absolute())
            item['vulnerable_code'] = code_list
            item['file_name'] = os.path.basename(file_path)
            print(item)
            file_handler.save_data(PersistencePath.vul_cfg_info,
                                   'fix_' + path.replace(PersistencePath.vul_cfg_info, ''), item)


# 获取已编译好的源码AST（CFG）
def get_cfg_data(path):
    bytecode_location_info = file_handler.read_data(f'{PersistencePath.vul_cfg_info}DAppSCAN_bytecode.jsonl')
    vulnerable_info_data = file_handler.read_data(path)
    for item in vulnerable_info_data:
        info = {'node_name': item['node_name'], 'file_name': Path(item['file_path']).name}
        vul_info = {'vul_type': item['vul_type'], 'vul_location': item['vul_location'],
                    'function': item['function'],
                    'vulnerable_code': item['vulnerable_code']}
        info['vulnerable_info'] = vul_info
        node_name = item['node_name']
        source_path = item['file_path']
        source_code = read_solidity(source_path)
        info['body'] = remove_comments(source_code)
        project_name = source_path.split('\\')[6]
        for item2 in bytecode_location_info:
            if node_name in item2.keys() and project_name in item2[node_name]:
                ast_data = file_handler.read_data(item2[node_name])
                sol_name = file_handler.get_file_name(source_path)
                for item3 in ast_data['sources'].keys():
                    if sol_name in item3:
                        ast = ast_data['sources'][item3]['AST']
                        info['AST'] = remove_id_src_fields(ast)
        file_handler.save_data(PersistencePath.Source_Code_Info,file_handler.get_file_name(path).replace('fix_','').replace('vulnerable_info_',''), info)


def remove_id_src_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    递归地移除AST数据中的所有id和src字段

    Args:
        data: 要处理的AST数据字典

    Returns:
        处理后的数据字典，不包含id和src字段
    """
    if not isinstance(data, dict):
        return data

    # 创建新字典，排除id和src字段
    result = {}
    for key, value in data.items():
        if key not in ['id', 'src', 'documentation', 'comments', 'StructuredDocumentation', 'text', 'absolutePath',
                       'exportedSymbols', 'license', 'scope', 'nameLocation']:
            if isinstance(value, dict):
                result[key] = remove_id_src_fields(value)
            elif isinstance(value, list):
                result[key] = [remove_id_src_fields(item) if isinstance(item, dict) else item for item in value]
            else:
                result[key] = value
    return result


def calculate_token(message):
    # 选择对应的编码方式（不同模型可能使用不同编码）
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4、GPT-3.5 等常用此编码

    tokens = encoding.encode(message)
    print(len(tokens))  # 输出：3（"Hello", ",", " world!" 对应 3 个 token）



# 控制流图实验数据准备
if __name__ == '__main__':
    # 提取漏洞基础信息
    data_path = PersistencePath.Vul_cfg_base
    save_file_name = 'DAppScan_vulnerable_info_cfg.jsonl'
    extract_dir_cfg(data_path, save_file_name)

    # 根据漏洞类型切分
    divide_vulnerable(PersistencePath.vul_cfg_info+save_file_name)

    # 提取编译后的字节码
    collect_ast_data_from_bytecode(PersistencePath.Vul_Source_bytecode_Base, '.json')

    # 补充漏洞位置源码信息
    for vul_type in VulnerabilityType:
        get_vulnerable_info_cfg(
            f'{PersistencePath.vul_cfg_info}DAppScan_{vul_type}_vulnerable_info_cfg.jsonl')

    # 补充漏洞文件源码以及对应的字节码
    for vul_type in VulnerabilityType:
        get_cfg_data(
            f'{PersistencePath.vul_cfg_info}fix_DAppScan_{vul_type}_vulnerable_info_cfg.jsonl')

