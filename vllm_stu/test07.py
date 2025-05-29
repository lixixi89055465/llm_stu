# -*- coding: utf-8 -*-
# @Time : 2025/5/26 20:34
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1GdX6YGEnZ?t=1431.3
# @File : test07.py
# @Software: PyCharm 
# @Comment :

from openai import OpenAI

model = OpenAI(base_url='http://localhost:8000/v1/', api_key='empty')
# model = OpenAI(base_url='http://localhost:8000/', api_key='empty')

resp = model.chat.completions.create(
    # model='/home/nanji/workspace/Qwen2.5-0.5B-Instruct',
    model="qwen2_5_1_5",
    messages=[{'role': 'user', 'content': '你好，给我介绍一下阿里巴巴'}]
)
print(resp.choices[0].message.content)
