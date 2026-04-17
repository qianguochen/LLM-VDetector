"""
分片策略模块
实现不同的内容分片算法
"""
import json
from typing import Dict, Any

from utils import file_handler
from collections import deque
from utils import token_utils


from .function_slicer import FunctionSlicer

def chunk_ast(ast_data):
    """
    Args:
        ast_data: AST数据（字符串或字典）
        chunk_size: 每个分片的最大token数

    Returns:
        list: 分片后的AST JSON字符串列表
    """
    # 处理输入数据，确保是字典格式
    if isinstance(ast_data, str):
        data = _remove_id_src_fields(json.loads(ast_data))
    else:
        data = _remove_id_src_fields(ast_data)

    chain_clusters_contract = {}
    build_call_graph_result = _build_call_graph(data)
    function_ast_nodes = build_call_graph_result[1]
    for key, value in build_call_graph_result[0].items():
        chain_clusters = cluster_by_call_chain(value)
        chain_clusters_contract[key] = chain_clusters

    data = remove_function_definitions(data)
    slicer = FunctionSlicer(chain_clusters_contract,build_call_graph_result[2],100000 - token_utils.estimate_tokens(json.dumps(data)))
    slices = slicer.slice_functions()
    chunks = []

    for item in slices:
        count_tokes = 0
        for item2 in item:
            contract = item2.split('.')[0]
            function = item2.split('.')[1]
            node = function_ast_nodes.get(contract).get(function)
            count_tokes += token_utils.estimate_tokens(json.dumps(node))
            if 'nodes' in data.keys():
                for contract_node in data['nodes']:
                    if contract_node.get('nodeType') == 'ContractDefinition':
                        if contract_node.get('name') == contract:
                            contract_node['nodes'].append(node)
            else:
                for contract_node in data['children']:
                    if contract_node.get('name') == 'ContractDefinition':
                        if contract_node.get('attributes').get('name') == contract:
                            contract_node['children'].append(node)
        chunks.append(json.dumps(data))
        data = remove_function_definitions(data)
    return chunks,slices


def remove_function_definitions(ast_dict):
    """删除AST中的FunctionDefinition节点"""
    if not isinstance(ast_dict, dict):
        return ast_dict

    # 如果是FunctionDefinition节点，返回None表示删除
    if ast_dict.get('nodeType') == 'FunctionDefinition' or ast_dict.get('name') == 'FunctionDefinition':
        return None

    # 递归处理所有子节点
    result = {}
    for key, value in ast_dict.items():
        if isinstance(value, dict):
            processed = remove_function_definitions(value)
            if processed is not None:  # 只保留非None的结果
                result[key] = processed
        elif isinstance(value, list):
            # 处理列表中的节点
            processed_list = []
            for item in value:
                if isinstance(item, dict):
                    processed_item = remove_function_definitions(item)
                    if processed_item is not None:
                        processed_list.append(processed_item)
                else:
                    processed_list.append(item)
            result[key] = processed_list
        else:
            result[key] = value

    return result


def _build_call_graph(ast_data):
    """
    构建合约内部的函数调用图
    Returns: dict {function_name: [called_functions]}
    """

    tokens_contract = {}
    if isinstance(ast_data, str):
        data = json.loads(ast_data)
    else:
        data = ast_data
    # 首先收集所有函数
    all_contract_functions = {}
    if 'nodes' in data.keys():
        for node in data.get('nodes', []):
            if node.get('nodeType') == 'ContractDefinition':
                functions = {}
                tokens = {}
                contract_name = node.get('name')
                print(contract_name)
                for node2 in node.get('nodes', []):
                    if node2.get('nodeType') == 'FunctionDefinition':
                        func_name = node2.get('name', 'constructor')
                        tokens[func_name] = token_utils.estimate_tokens(node2)
                        functions[func_name] = node2
                all_contract_functions[contract_name] = functions
                tokens_contract[contract_name] = tokens
    else:
        for node in data.get('children', []):
            if node.get('name') == 'ContractDefinition':
                contract_name = node.get('attributes').get('name')
                print(contract_name)
                functions = {}
                tokens = {}
                for node2 in node.get('children', []):
                    if node2.get('name') == 'FunctionDefinition':
                        func_name = node2.get('attributes').get('name')
                        tokens[func_name] = token_utils.estimate_tokens(node2)
                        functions[func_name] = node2
                all_contract_functions[contract_name] = functions
                tokens_contract[contract_name] = tokens

    call_graph_contract = {}
    for key,value in all_contract_functions.items():
        call_graph = {}
        for func_name in value:
            call_graph[func_name] = []
        call_graph_contract[key]  = call_graph

    # 分析每个函数的调用关系
    for key,value in all_contract_functions.items():
        for func_name, func_node in value.items():
            called_functions = _extract_called_functions(func_node, value.keys())
            call_graph_contract.get(key)[func_name] = called_functions

    return call_graph_contract, all_contract_functions, tokens_contract


def _extract_called_functions(func_node, all_functions):
    """提取函数中调用的其他函数"""
    called_functions = set()

    def traverse_node(node):
        if isinstance(node, dict):
            if 'nodeType' in node.keys():
                # 检查是否是函数调用
                if (node.get('nodeType') == 'FunctionCall' and
                        node.get('expression', {}).get('nodeType') == 'Identifier'):
                    called_name = node['expression'].get('name')
                    if called_name in all_functions:
                        called_functions.add(called_name)

                # 递归遍历子节点
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        traverse_node(value)
            else:
                for child in node.get('children', []):
                    if child.get('name') == 'FunctionCall':
                        for child2 in child.get('children', []):
                            if child2.get('name') == 'Identifier':
                                if 'function' in child2.get('attributes').get('type'):
                                    called_name = child2.get('attributes').get('value')
                                    if called_name in all_functions:
                                        called_functions.add(called_name)

                        # 递归遍历子节点
                    for key, value in child.items():
                        if isinstance(value, (dict, list)):
                            traverse_node(value)

        elif isinstance(node, list):
            for item in node:
                traverse_node(item)

    traverse_node(func_node)
    return list(called_functions)


def cluster_by_call_chain(call_graph):
    """
    基于调用链进行聚类
    """
    visited = set()
    clusters = []

    for func in list(call_graph.keys()):
        if func not in visited:
            # 找到所有相关的函数（调用链）
            cluster = _find_related_functions(func, visited, call_graph)
            if cluster:
                clusters.append(cluster)

    return clusters


def _find_related_functions(start_func, visited, call_graph):
    """找到与起始函数相关的所有函数"""
    if start_func in visited:
        return []

    cluster = set()
    queue = deque([start_func])

    function_to_index = {func: idx for idx, func in enumerate(call_graph.keys())}

    while queue:
        current = queue.popleft()
        if current in visited:
            continue

        visited.add(current)
        cluster.add(current)

        # 添加被调用的函数
        for callee in call_graph.get(current, []):
            if callee not in visited and callee in function_to_index:
                queue.append(callee)

        # 添加调用当前函数的函数
        for caller, callees in call_graph.items():
            if current in callees and caller not in visited and caller in function_to_index:
                queue.append(caller)

    return sorted(list(cluster))


def _remove_id_src_fields(data: Dict[str, Any]) -> Dict[str, Any]:
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
                result[key] = _remove_id_src_fields(value)
            elif isinstance(value, list):
                result[key] = [_remove_id_src_fields(item) if isinstance(item, dict) else item for item in value]
            else:
                result[key] = value
    return result


if __name__ == '__main__':
    ast_data = file_handler.read_data(
        '../DAppSCAN_CFG/vulnerable_info_data_for_gpt/DAppScan_Authorization_through_tx.origin_vulnerable_cfg_info_AST.jsonl')
    result = chunk_ast(ast_data[0]['AST'])
    # print(ast_data[2])
    # print(result[0])
    # print(result[2])
    # chain_clusters = cluster_by_call_chain(result[0])
    # print(chain_clusters)
    # for i, cluster_funcs in enumerate(chain_clusters, 1):
    #     print(f"调用链簇 {i}: {cluster_funcs}")
    # print(result[1])
