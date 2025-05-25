# -*- coding: utf-8 -*-
# @Time : 2025/5/25 16:06
# @Author : nanji
# @Site : https://blog.csdn.net/zjkpy_5/article/details/145802029
# @File : test03.py
# @Software: PyCharm 
# @Comment :
import requests
import json

# 设置请求的URL
url = "http://localhost:8000/v1/completions"

# 设置请求头部
headers = {
    "Content-Type": "application/json"
}

# 准备请求数据
data = {
    "model": "qwen2_5_1_5",
    "prompt": "你好，你是？",
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 0.8,
    "repetition_penalty": 1.05
}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 检查响应状态并打印结果
if response.status_code == 200:
    try:
        # 尝试解析响应中的 'choices' 字段，并获取生成的文本
        choices = response.json().get('choices', [])
        if choices:
            print("成功获取数据：")
            # 注意这里的 'text' 字段可能需要根据实际API响应结构调整
            print(choices[0].get('text', ''))
        else:
            print("没有获取到任何选择结果")
    except json.JSONDecodeError:
        print("无法解析JSON响应")
else:
    print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")