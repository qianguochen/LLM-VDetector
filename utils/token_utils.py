"""
Token处理工具模块
负责token估算和限制检查
"""
import json

import tiktoken
from config.settings import MODEL_NAME


def get_encoding(model=MODEL_NAME):
    """获取指定模型的token编码器"""
    return tiktoken.encoding_for_model(model)


def estimate_tokens(text, model=MODEL_NAME):
    """
    准确估算文本的token数量

    Args:
        text: 要估算的文本
        model: 模型名称

    Returns:
        int: token数量
    """
    try:
        encoding = get_encoding(model)
        if isinstance(text, dict):
            data = json.dumps(text)
        else:
            data = text
        return len(encoding.encode(data))
    except Exception:
        # 备用方案：简单估算（4个字符约等于1个token）
        return len(text) // 4

