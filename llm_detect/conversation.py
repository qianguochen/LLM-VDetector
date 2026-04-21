"""
会话管理模块
处理多轮对话和上下文维护
"""
from api_client import LLMClient


class ConversationManager:
    """会话管理器，处理长上下文对话"""

    def __init__(self):
        """
        初始化会话管理器
        """
        self.client = LLMClient()

    def process_detection(self, message, vulnerable_info):
        try:
            return self.client.execute_detect(message[0], message[1], vulnerable_info)
        except Exception as e:
            print(e)
        return {}
