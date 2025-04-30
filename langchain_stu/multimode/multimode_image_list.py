# -*- coding: utf-8 -*-
# @Time : 2025/4/30 16:53
# @Author : nanji
# @Site : 
# @File : multimode_image_list.py
# @Software: PyCharm 
# @Comment :
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
# 加载环境变量
import os
import base64
import httpx
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'

image_url_1 = 'https://img2.baidu.com/it/u=1207683725,4212532757&fm=253&fmt=auto&app=120&f=JPEG?w=710&h=500'
image_data_1 = base64.b64encode(httpx.get(image_url_1).content).decode('utf-8')

image_url_2 = 'https://img2.baidu.com/it/u=3176117005,4167037938&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=889'
image_data_2 = base64.b64encode(httpx.get(image_url_2).content).decode('utf-8')
model = ChatOpenAI(model='gpt-4o')
message = HumanMessage(
    content=[
        {'type': 'text', 'text': '这两张图片是一样的吗？'},
        # {'type': 'text', 'image_url': image_url_1},
        {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_data_1}"}},
        {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_data_2}"}},
    ]
)
response = model.invoke([message])
print(response.content)
