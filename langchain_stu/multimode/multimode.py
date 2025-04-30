# -*- coding: utf-8 -*-
# @Time : 2025/4/30 16:08
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9?spm_id_from=333.788.player.switch&vd_source=50305204d8a1be81f31d861b12d4d5cf&p=6
# @File : multimode.py
# @Software: PyCharm 
# @Comment :
# 加载环境变量
import os

os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'

import base64
import httpx
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

image_url = 'https://pic.rmb.bdstatic.com/bjh/down/eQdGNnAyTDeUuqA2oRcsWg03fa619d190ff3d14f3937ab8518ad57.jpg'
# image_data = base64.b64encode(httpx.get(image_url).content).decode('utf-8')
image_data = base64.b64encode(httpx.get(image_url).content).decode('utf-8')
model = ChatOpenAI(model='gpt-4o')
message = HumanMessage(
    content=[
        {'type': 'text', 'text': '用中文描述这张图片中的天气'},
        # {'type': 'image_url', 'image_url': {'url': image_url}}
        {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_data}"}}
    ]
)
response = model.invoke([message])
print(response.content)
# 这张图片中的天气看起来像是阴天，有下雨的迹象。树木和周围的环境似乎湿漉漉的，可能是因为正在下雨或者刚刚下过雨。天空中云层较厚，阳光被遮挡住，整体氛围比较阴暗。
