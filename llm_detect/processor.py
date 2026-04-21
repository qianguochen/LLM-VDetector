"""
AST专用处理模块
针对Solidity AST的特殊处理逻辑
"""
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor

from config.settings import MAX_WORKERS,DETECT_MODES
from conversation import ConversationManager
from config import prompt
from config.enums import DetectMode
from params import DetectParams
from utils import file_handler
from chunk_strategies import chunk_ast
from data_preparation import smart_contract_parser as parser

def _vuln_to_hash(vuln_dict):
    """将漏洞字典转为短哈希值"""
    # 1. 将字典转为排序后的JSON字符串（保证相同内容生成相同哈希）
    vuln_str = json.dumps(vuln_dict, sort_keys=True)
    # 2. 计算MD5（取前8位或16位）
    hash_obj = hashlib.md5(vuln_str.encode())
    return hash_obj.hexdigest()[:8]  # 8位十六进制，足够避免短碰撞

def _build_request_params(self, data):
    source_code = data['body']
    ast_data = {}
    if 'AST' in data.keys():
        ast_data = data['AST']
    vul_type = self.params.get_vul_type().replace('_', ' ')
    if self.mode == DetectMode.SOURCE_ONLY:
        content_message = f"Analyze the possible risks of {vul_type} in these codes:{source_code}"
        return prompt.prompt_system_code, content_message
    elif self.mode == DetectMode.CFG_ONLY:

        content_message = f"Analyze the AST data of the following Solidity contract to identify potential {vul_type} vulnerability risks:{ast_data}"
        return prompt.prompt_system_ast, content_message
    else:

        content_message = f"Source Code:{source_code}; AST Analysis:{ast_data}. Analyze the  Solidity contract code and the AST data of the following Solidity contract provided above to identify {vul_type} vulnerability risks:"
        return prompt.prompt_system_ast_source_code, content_message


class ASTProcessor:
    """AST专用处理器，用于Solidity代码分析"""

    def __init__(self):
        """
        初始化AST处理器

        Args:

        """
        self.mode = DETECT_MODES
        self.conversation_manager = ConversationManager()
        self.params = DetectParams(DETECT_MODES)
        self.executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    def analyze_vulnerabilities(self):
        """
        分析AST中的安全漏洞

        Args:
        Returns:
            list: 漏洞列表

        """
        # 使用会话管理器处理
        vul_type = self.params.get_vul_type()
        vul_source_code_path = self.params.get_source_code_path()
        output_dir = self.params.get_output_dir()
        future_results = []
        if self.mode == DetectMode.SOURCE_ONLY:
            had_detected = list({
                _vuln_to_hash(item[0]['vulnerable_info'])
                for item in file_handler.read_data(f'{output_dir}DAppScan_{vul_type}_result.jsonl')
            })
            data = file_handler.read_data(f'{vul_source_code_path}DAppScan_{vul_type}.jsonl')
            for item in data:
                results = []
                if _vuln_to_hash(item['vulnerable_info']) in had_detected:
                    continue
                message = _build_request_params(self, item)
                future =  self.executor.submit(self.conversation_manager.process_detection, message,item)
                results.append(future.result())
                future_results.append(results)
            file_handler.save_data(output_dir, f'DAppScan_{vul_type}_result.jsonl', future_results)
        elif self.mode == DetectMode.CFG_ONLY:
            had_detected = list({
                _vuln_to_hash(item[0]['vulnerable_info'])
                for item in file_handler.read_data(f'{output_dir}DAppScan_{vul_type}_result.jsonl')
            })
            data = file_handler.read_data(f'{vul_source_code_path}DAppScan_{vul_type}_cfg.jsonl')

            for item in data:
                results = []
                if _vuln_to_hash(item['vulnerable_info']) in had_detected:
                    continue
                chunks = chunk_ast(item['AST'])
                for chunk in chunks[0]:
                    item['AST'] = chunk
                    message = _build_request_params(self, item)
                    future = self.executor.submit(self.conversation_manager.process_detection, message, item)
                    results.append(future.result())
                future_results.append(results)
            file_handler.save_data(output_dir, f'DAppScan_{vul_type}_result.jsonl', future_results)
        else:
            had_detected = list({
                _vuln_to_hash(item[0]['vulnerable_info'])
                for item in file_handler.read_data(f'{output_dir}DAppScan_{vul_type}_result.jsonl')
            })
            data = file_handler.read_data(f'{vul_source_code_path}DAppScan_{vul_type}_cfg.jsonl')
            for item in data:
                results = []
                if _vuln_to_hash(item['vulnerable_info']) in had_detected:
                    continue
                chunks_info = chunk_ast(item['AST'])
                source_code = item['body']
                source_code_filter = parser.filter_function_bodies(source_code, chunks_info[1])
                for i in range(len(chunks_info[0])):
                    item['AST'] = chunks_info[0][i]
                    item['body'] = source_code_filter[i]
                    message = _build_request_params(self, item)
                    future = self.executor.submit(self.conversation_manager.process_detection, message, item)
                    results.append(future.result())
                future_results.append(results)
            file_handler.save_data(output_dir, f'DAppScan_{vul_type}_result.jsonl', future_results)
