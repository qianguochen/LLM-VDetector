import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
from utils import file_handler
from config import enums

lock = threading.Lock()


def read_solidity(file):
    path = Path(file)
    with open(fr"\\?\{path.absolute()}", 'r', encoding='utf-8') as f:
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


def task(last_folder_name, file_name, path, vulnerable_info):
    solidity_code = read_solidity(path)
    code_without_single_line_comments = re.sub("//.*$", "", solidity_code, flags=re.MULTILINE)
    code_without_multi_line_comments = re.sub("/\*.*?\*/", "", code_without_single_line_comments, flags=re.DOTALL)
    smart_contract_info = {'name': file_name, 'vulnerable_info':vulnerable_info,'file_path': path, 'body': code_without_multi_line_comments}
    # print(smart_contract_info)
    file_handler.save_data(last_folder_name, smart_contract_info)

if __name__ == '__main__':

    thread = 10
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\Authorization through tx.origin')
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\Delegatecall to Untrusted Callee')
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\Integer Overflow and Underflow')
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\Presence of unused variables')
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\Reentrancy')
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\Transaction Order Dependence')
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\\Unchecked Call Return Value')
    # sol_info = extract_dir('F:\pycharmprojectforwork\SCVR-AI\DAppScan_Contracts\\Unprotected Ether Withdrawal')
    # with ThreadPoolExecutor(max_workers=thread) as executor:
    #     save_name = sol_info[1]
    #     for file, path in sol_info[0].items():
    #         executor.submit(task(save_name, file, path))
    vulnerable_type = enums.VulnerabilityType.Unprotected_Ether_Withdrawal
    save_path = f'DAppSCAN/vulnerable_info_data_for_gpt/{vulnerable_type}.jsonl'
    file_handler.init_file(save_path)
    path = f'E:\Project\PycharmProjects\SCVR-AI\DAppSCAN\\vulnerable_info_data_origin\DAppScan_{vulnerable_type}_vulnerable_info.jsonl'
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        for item in data:
            vulnerable = json.loads(item)
            absolute_path = vulnerable['file_path']
            vulnerable_info = vulnerable['vulnerable_info']
            file_name = Path(absolute_path).name
            print(file_name)
            with ThreadPoolExecutor(max_workers=thread) as executor:
                executor.submit(task(save_path, file_name, absolute_path, vulnerable_info))