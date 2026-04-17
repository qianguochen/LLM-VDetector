"""
会话管理模块
处理多轮对话和上下文维护
"""
from .chunk_strategies import chunk_ast
from .api_client import LLMClient
import re
from config import prompt

class ConversationManager:
    """会话管理器，处理长上下文对话"""

    def __init__(self, api_key=None, base_url=None):
        """
        初始化会话管理器

        Args:
            api_key: OpenAI API密钥
        """
        self.client = LLMClient(api_key, base_url)

    def process_long_content(self, content, user_message,vulnerable_info):
        """
        处理超长内容的核心方法
        Args:
            content: 要处理的长内容
            user_message: 用户指令
            content_type: 内容类型（text/ast_json）

        Returns:
            str: 处理结果
        """
        results = []
        # 选择分片策略
        chunks =  chunk_ast(content)
        for chunk in chunks:
            result =  self._process_single_chunk(chunk, user_message,vulnerable_info)
            results.append(result)
        return results

    def _process_single_chunk(self, chunk, user_message,vulnerable_info):
        """处理单块内容"""
        full_prompt = f"{user_message}\n{chunk}{prompt.prompt_answer_ast}"
        return  self.client.execute_detect(full_prompt,vulnerable_info)

