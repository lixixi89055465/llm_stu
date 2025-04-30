# -*- coding: utf-8 -*-
# @Time : 2025/4/30 17:05
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9?spm_id_from=333.788.player.switch&vd_source=50305204d8a1be81f31d861b12d4d5cf&p=6
# @File : tools_call.py
# @Software: PyCharm 
# @Comment :

from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
import base64
import httpx
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

@tool
def weather_tool(weather: Literal['晴朗的', '多云的', '多雨的', '下雪的']) -> None:
    pass


model = ChatOpenAI(model='gpt-4o')
model_with_tools = model.bind_tools([weather_tool])
image_url_1 = 'https://img2.baidu.com/it/u=1207683725,4212532757&fm=253&fmt=auto&app=120&f=JPEG?w=710&h=500'
image_data_1 = base64.b64encode(httpx.get(image_url_1).content).decode('utf-8')

image_url_2 = 'https://img2.baidu.com/it/u=3176117005,4167037938&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=889'
image_data_2 = base64.b64encode(httpx.get(image_url_2).content).decode('utf-8')

message=HumanMessage(
    content=[
        {'type': 'text', 'text': '用中国问描述两张图片中的天气？'},
        {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_data_1}"}},
        {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{image_data_2}"}},
    ]
)
response=model_with_tools.invoke([message])
print(response.tool_calls)