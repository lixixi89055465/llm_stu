# -*- coding: utf-8 -*-
# @Time : 2025/5/25 16:30
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1GdX6YGEnZ?t=1456.1
# @File : test06.py
# @Software: PyCharm 
# @Comment :

from openai import OpenAI
model=OpenAI(base_url='http://127.0.0.1:8000/v1/',api_key='empty')
resp=model.chat.completions.create(
    model='',
    messages=[{'role': 'user', 'content': '你好，请介绍一下阿里巴巴!'}]
)
