# -*- coding: utf-8 -*-
# @Time : 2025/5/25 15:45
# @Author : nanji
# @Site : https://blog.csdn.net/zjkpy_5/article/details/145802029
# @File : test02.py
# @Software: PyCharm 
# @Comment :

from openai import OpenAI

# 设置 OpenAI 的 API key 和 API base 来使用 vLLM 的 API server.
openai_api_key = "EMPTY"  # 如果不需要 API key，可以留空或设置为 "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 创建 Completion 请求
completion_response = client.completions.create(
    model="qwen2_5_1_5",
    prompt="你好，你是？",
    max_tokens=2048,
    temperature=0.7,
    top_p=0.8,
    extra_body={"repetition_penalty": 1.05},
)

# 检查响应并打印结果
if hasattr(completion_response, 'choices') and len(completion_response.choices) > 0:
    print("成功获取数据：")
    print(completion_response.choices[0].text)
else:
    print(f"请求失败，响应内容：{completion_response}")