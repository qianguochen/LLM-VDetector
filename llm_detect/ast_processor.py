"""
AST专用处理模块
针对Solidity AST的特殊处理逻辑
"""
import json

from .conversation import ConversationManager
from config import prompt

class ASTProcessor:
    """AST专用处理器，用于Solidity代码分析"""

    def __init__(self, api_key=None, base_url=None):
        """
        初始化AST处理器

        Args:
            api_key: OpenAI API密钥
        """
        self.conversation_manager = ConversationManager(api_key, base_url)



    def analyze_vulnerabilities(self, ast_json,vulnerability_type,vulnerable_info):
        """
        分析AST中的安全漏洞

        Args:
            ast_json: AST数据
            specific_checks: 特定检查项列表

        Returns:
            list: 漏洞列表
        """
        # 使用会话管理器处理
        user_message = self._build_analysis_message(vulnerability_type)
        result =  self.conversation_manager.process_long_content(
            ast_json, user_message,vulnerable_info
        )
        return result



    def _build_analysis_message(self,vulnerability_type):
        """构建分析提示消息"""
        message = f'{prompt.prompt_start_ast}{prompt.prompt_vulnerable_type_ast[vulnerability_type]}'
        return message
