# -*- coding: utf-8 -*-
# @Time : 2025/5/24 08:17
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1GdX6YGEnZ?t=1550.9
# @File : test01.py
# @Software: PyCharm 
# @Comment :
from openai import OpenAI

model = OpenAI(
    api_key='empty',
    base_url='http://localhost:8000/v1/',
)

# completion_response = model.chat.completions.create(
completion_response = model.completions.create(
#     model='/home/nanji/workspace/Qwen2.5-0.5B-Instruct',
    model="qwen2_5_1_5",
    # messages=[
    #     {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    #     {"role": "user", "content": "你是谁？"},
    # ],
    prompt="你好，你是？",
    temperature=0.7,
    top_p=0.8,
    max_tokens=512,
    extra_body={
        "repetition_penalty": 1.05,
    },
)
# print(resp.choices[0].message.content)

# 检查响应并打印结果
if hasattr(completion_response, 'choices') and len(completion_response.choices) > 0:
    print("成功获取数据：")
    print(completion_response.choices[0].text)
else:
    print(f"请求失败，响应内容：{completion_response}")