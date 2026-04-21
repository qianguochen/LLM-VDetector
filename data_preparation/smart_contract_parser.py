import regex as re
from pygments.lexers import SolidityLexer
from pygments.token import Token


def read_solidity(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def cut_function_bodies(solidity_code):
    lexer = SolidityLexer()
    tokens = list(lexer.get_tokens(solidity_code))
    function_bodies = []
    in_function = False
    token_values = ''
    for token_type, token_value in tokens:
        if in_function:
            if token_value == 'function':
                function_bodies.append(token_values)
                token_values = 'function'
                in_function = False
            else:
                token_values += token_value
        else:
            if token_value == 'function':
                function_bodies.append(token_values)
                token_values = 'function'
                in_function = True
            else:
                token_values += token_value

    function_bodies.append(token_values)
    return function_bodies


def filter_function_bodies(solidity_code, slice_functions):
    lexer = SolidityLexer()
    tokens = list(lexer.get_tokens(solidity_code))

    filtered_code = []
    in_function = False
    brace_count = 0
    brace_count_contract = 0
    function_start = False
    function_tokens = []
    current_function = ''
    count_name_variable = 0
    in_contract = False
    contract_start = False
    current_contract = ''
    result_list = []

    for item in slice_functions:
        count_function = 0
        for token_type, token_value in tokens:
            # 检测 function 关键字
            # print(token_type, token_value)
            if token_type == Token.Keyword.Type and token_value == 'function' and in_contract:
                in_function = True
                function_start = True
                brace_count = 0
                function_tokens = []

            if token_type == Token.Keyword and token_value == 'contract':
                in_contract = True
                contract_start = True
                brace_count_contract = 0

            if in_contract:
                if token_type == Token.Name.Entity:
                    current_contract = token_value
                if token_value == '{':
                    brace_count_contract += 1
                elif token_value == '}':
                    brace_count_contract -= 1
                    if brace_count_contract == 0 and contract_start:
                        in_contract = False
                        contract_start = False

            if in_function and in_contract:
                if token_type == Token.Name.Variable and count_name_variable == 0:
                    current_function = token_value
                    count_name_variable += 1
                function_tokens.append((token_type, token_value))
                # 统计大括号数量
                if token_value == '{':
                    brace_count += 1
                elif token_value == '}':
                    brace_count -= 1
                    # 当大括号数量归零时，函数体结束
                    if brace_count == 0 and function_start:
                        in_function = False
                        function_start = False
                        count_name_variable = 0
                        # 将完整的函数添加到结果中
                        if current_contract + '.' + current_function in item:
                            count_function += 1
                            for t_type, t_value in function_tokens:
                                if t_type != Token.Comment.Single and t_type != Token.Comment.Multiline:
                                    if t_type == Token.Text.Whitespace:
                                        t_value = re.sub('\n+', '', t_value)
                                        t_value = re.sub(' +', ' ', t_value)
                                        filtered_code.append((t_type, t_value))
                                    else:
                                        filtered_code.append((t_type, t_value))

                        function_tokens = []

            # 如果不在函数中，保留其他代码
            else:
                if token_type != Token.Comment.Single and token_type != Token.Comment.Multiline:
                    if token_type == Token.Text.Whitespace:
                        token_value = re.sub('\n+', '', token_value)
                        token_value = re.sub(' +', ' ', token_value)
                        filtered_code.append((token_type, token_value))
                    else:
                        filtered_code.append((token_type, token_value))

        # 将过滤后的 tokens 转换回代码字符串
        result = ''.join(token_value for _, token_value in filtered_code)
        if count_function == 0:
            print('源码文件与AST文件不对应')
        result_list.append(result)
    return result_list





