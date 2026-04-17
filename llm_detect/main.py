"""
主程序入口模块
演示如何使用长上下文处理功能
"""

import json

# from judge_gpt_vulnerable_detect_cfg import fix_vulnerable_info
from ast_processor import ASTProcessor
from utils import file_handler
from config import prompt


def main():
    """主函数示例"""
    vulnerability_type = prompt.VulnerabilityType.Outdated_Compiler_Version
    ast_data = file_handler.read_data(
        f'../DAppSCAN_CFG/vulnerable_info_data_for_gpt/DAppScan_{vulnerability_type}_vulnerable_cfg_info_AST.jsonl')

    ast_processor = ASTProcessor()

    # save_path = vulnerability_type + '_DAppSCAN_optimization_prompt_cfg.jsonl'
    save_path = f'../DAppSCAN_CFG/gpt_result/{vulnerability_type}_DAppSCAN_optimization_prompt_cfg.jsonl'
    check_result = f'../DAppSCAN_CFG/check_result/DAppSCAN_vulnerable_{vulnerability_type}_result.jsonl'
    source_path = set()
    had_detected = file_handler.read_data(save_path)
    had_checked = file_handler.read_data(check_result)
    for line in had_detected:
        source_path.add(line[0]['vulnerable_info']['sourcePath'])
    for item in ast_data:
        path = item['vulnerable_info']['sourcePath']
        if path not in source_path:
            source_path.add(path)
            result = ast_processor.analyze_vulnerabilities(
                item['AST'],
                vulnerability_type,
                item['vulnerable_info']
            )
            print(result)
            file_handler.save_data(save_path, result)


# def process_recheck():
#
#     vulnerability_type = prompt.VulnerabilityType.Integer_Overflow_and_Underflow
#     source_path = 'rce/contracts/consensys-ENS_Permanent_Registrar/ethregistrar-e52abfc2799ac361364aca6135fc20f9175a29fd/contracts/SimplePriceOracle.sol'
#
#     ast_data = file_handler.read_data(
#         f'../DAppSCAN_CFG/vulnerable_info_data_for_gpt/DAppScan_{vulnerability_type}_vulnerable_cfg_info_AST.jsonl')
#
#     ast_processor = ASTProcessor()
#     save_path = f'../DAppSCAN_CFG/gpt_result/{vulnerability_type}_DAppSCAN_optimization_prompt_cfg.jsonl'
#     fix_vulnerable_info_data = file_handler.read_data(
#         f'../DAppSCAN_CFG/fix_vulnerable_info_data_for_comparison/fix_DAppScan_{vulnerability_type}_vulnerable_cfg_info.jsonl')
#
#     for item in fix_vulnerable_info(fix_vulnerable_info_data):
#         sourcePath = item['source_path']
#         if sourcePath == source_path:
#             print('origin_result:')
#             for item3 in item['vulnerable_info']:
#                 print(item3['function'])
#                 print(item3['lines'])
#                 for code_line in item3['vulnerable_code']:
#                     print(code_line)
#
#     aim_ast_data = {}
#     for item in ast_data:
#         path = item['vulnerable_info']['sourcePath']
#         node_name = item['node_name']
#         # if path == source_path and node_name == 'EchidnaTester.json':
#         if path == source_path:
#             aim_ast_data = item
#     result = ast_processor.analyze_vulnerabilities(
#         aim_ast_data['AST'],
#         vulnerability_type,
#         aim_ast_data['vulnerable_info']
#     )
#     print('gpt_result:')
#     for item4 in result:
#         if item4['result']['result'].lower() == 'yes':
#             for item5 in item4['result']['vulnerabilities']:
#                 print(f"function :  {item5['location']['function']}")
#                 print(f"code     :{item5['location']['code']}")
#             # for item5 in item4['result']['vulnerable_code']:
#             #     print(f"code     :{item5}")
#         else:
#             print(result)
#     flag = input("是否保存: ")
#     if flag == 'yes':
#         file_handler.save_data(save_path, result)


if __name__ == "__main__":
    # main()
    # process_recheck()
    pass