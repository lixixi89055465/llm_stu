# -*- coding: utf-8 -*-
# @Time : 2025/5/4 15:31
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?spm_id_from=333.1391.0.0&p=7&vd_source=50305204d8a1be81f31d861b12d4d5cf
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
    # 默认情况下，如果函数抛出ToolException,则将toolException 的message 作为响应
    # 如哦设置为True,将返回ToolException异常文本，False将会抛出ToolException
    handle_tool_error=True
)

response = get_weather_tool.invoke({'city': 'foobar'})
print(response)
