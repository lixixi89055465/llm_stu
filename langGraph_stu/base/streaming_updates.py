# -*- coding: utf-8 -*-
# @Time : 2025/6/23 23:01
# @Author : nanji
# @Site : 
# @File : streaming_updates.py
# @Software: PyCharm 
# @Comment :
import asyncio
from typing import Literal
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


# 定义一个工具函数，用于获取天气信息
@tool
def get_weather(city: Literal['nyc', 'sf']):
    ''' Use this to get weather information.'''
    if city == 'nyc':
        return "It might be cloudy in nyc"
    elif city == 'sf':
        return "It's always sunny in sf"
    else:
        raise AssertionError('Unknow city')


# 创建一个包含工具函数的列表
tools = [get_weather]

# 初始化一个OpenAI 的聊天模型，使用gpt-4o,温度设为0(生成结果更确定）
model = ChatOpenAI(model_name='gpt-4o', temperature=0)


# 定义一个异步主函数
async def main():
    # 创建一个反应式代理，使用聊天模型和工具
    graph = create_react_agent(model, tools)
