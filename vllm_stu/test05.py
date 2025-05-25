# -*- coding: utf-8 -*-
# @Time : 2025/5/25 16:22
# @Author : nanji
# @Site : https://blog.csdn.net/zjkpy_5/article/details/145802029
# @File : test05.py
# @Software: PyCharm 
# @Comment :
import requests
import json

# 设置API的基本URL和端点
base_url = "http://localhost:8000/v1"
endpoint = "/chat/completions"

url = base_url + endpoint

# 设置请求头部
headers = {
    "Content-Type": "application/json",
}

# 准备请求数据
data = {
    "model": "qwen2_5_1_5",
    "messages": [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
    "temperature": 0.7,
    "top_p": 0.8,
    "max_tokens": 512,
    "repetition_penalty": 1.05,  # 直接包含在请求体中
}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 检查响应状态并打印结果
if response.status_code == 200:
    print("Chat response:", response.json()['choices'][0]['message'])
else:
    print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")