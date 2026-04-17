"""
API客户端模块
负责与OpenAI API的通信
"""
import asyncio
import datetime
import re
import requests
from config.settings import API_KEY, API_URL, MODEL_NAME
import json


class LLMClient:
    """GPT-4o API客户端"""

    def __init__(self, api_key=None, base_url=None):
        """
        初始化API客户端

        Args:
            api_key: OpenAI API密钥，如果为None则使用环境变量
        """
        self.api_key = API_KEY
        self.base_url = API_URL

    def execute_detect(self, prompt, vulnerable_info):
        """
        调用GPT-4o API，包含重试机制

        Args:
            prompt: 提示词文本
            max_retries: 最大重试次数

        Returns:
            str: 模型响应内容

        Raises:
            Exception: 所有重试失败后抛出异常
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "messages": [{"role": "system", "content": prompt},{"role": "user", "content": prompt}],
            'model': MODEL_NAME,
            "temperature": 0.2
        }

        start_time = datetime.datetime.now()
        result_info = {}
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            end_time = datetime.datetime.now()
            time_taken = (end_time - start_time).total_seconds() * 1000
            response_json = response.json()
            result = response_json["choices"][0]["message"]["content"]
            result_json = json.loads(self._re_result(result))
            result_info['result'] = result_json
            prompt_tokens = response_json["usage"]["prompt_tokens"]
            completion_tokens = response_json["usage"]["completion_tokens"]
            result_info['vulnerable_info'] = vulnerable_info
            result_info['prompt_tokens'] = prompt_tokens
            result_info['completion_tokens'] = completion_tokens
            result_info['time'] = time_taken
            return result_info
        except Exception as e:
            print(e)


    def _re_result(self, result):
        try:
            result_patter = re.compile('(?P<gpt_result>\{.*\})', re.DOTALL)
            matches = result_patter.finditer(result)
            filter_result = ''
            for match in matches:
                filter_result = match.groupdict().get('gpt_result')
            return filter_result
        except Exception as e:
            print(e)
            return result
