# -*- coding: utf-8 -*-
# @Time : 2025/5/25 16:18
# @Author : nanji
# @Site : https://blog.csdn.net/zjkpy_5/article/details/145802029
# @File : test04.py
# @Software: PyCharm 
# @Comment :

from openai import OpenAI

# 设置 OpenAI 的 API key 和 API base 来使用 vLLM 的 API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

chat_response = client.chat.completions.create(
    model="qwen2_5_1_5",
    messages=[
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
    temperature=0.7,
    top_p=0.8,
    max_tokens=512,
    extra_body={
        "repetition_penalty": 1.05,
    },
)

# 直接访问响应对象的属性，而不是尝试调用 .json()
print("Chat response:", chat_response.choices[0].message.content)