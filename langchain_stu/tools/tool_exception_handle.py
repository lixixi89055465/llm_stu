# -*- coding: utf-8 -*-
# @Time : 2025/5/4 15:31
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9?t=969.6&p=7
# @File : tool_exception.py
# @Software: PyCharm 
# @Comment :

from langchain_core.tools import StructuredTool
# 导入工具出现异常的时候处理的库
from langchain_core.tools import ToolException


def get_weather(city: str) -> int:
    '''获取发给定城市的天气。'''
    raise ToolException(f'错误：没有名为{city}的城市')


get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error='没找到这个城市'
)

response = get_weather_tool.invoke({'city': 'foobar'})
print(response)
