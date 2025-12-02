import os
from typing import List, Dict

from openai import OpenAI


class LLMClient:
    """简单封装 OpenAI Chat Completions"""

    def __init__(
        self,
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 512,
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("环境变量 OPENAI_API_KEY 未设置")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """调用 Chat Completions，返回 content 文本"""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return resp.choices[0].message.content
