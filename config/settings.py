GPT = {"model": 'gpt-4o',
       "api_key": "sk-Zq367BUJF7Jx70**********d6MuUsqHtWMvh8ItwSXE8wtW",
       "api_url": "https://api.vectorengine.ai/v1/chat/completions"}

CodeLlama = {"model": 'llama-3-70b',
             "api_key": "sk-Zq367BUJF7**********WOFTd6MuUsqHtWMvh8ItwSXE8wtW",
             "api_url": "https://api.vectorengine.ai/v1/chat/completions"}

DeepSeek = {"model": 'deepseek-v3-1-250821',
            "api_key": "sk-tBxJnlMvuypo**********sBb4PgxvB99B7cmBZvUJZDSiZv",
            "api_url": "https://api.vectorengine.ai/v1/chat/completions"}

Claude = {"model": 'claude-sonnet-4-6',
          "api_key": "sk-Q4Hx9CKmCFDnfw**********ziGjKJIX2GORrPtX6DPBAYql",
          "api_url": "https://api.vectorengine.ai/v1/chat/completions"}


# 检测模式枚举
DETECT_MODES = {
    "SOURCE_ONLY": "source",           # 仅源码检测
    "CFG_ONLY": "cfg",                 # 仅控制流图检测
    "SOURCE_AND_CFG": "source_cfg",    # 源码 + 控制流图检测
}

