# -*- coding: utf-8 -*-
# @Time : 2025/5/2 22:42
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?p=7&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : tools_decorator.py
# @Software: PyCharm 
# @Comment :

# 导入工具装饰器库
from langchain_core.tools import tool



@tool
def multiply(a: int, b: int) -> int:
    '''Multiply two numbers.'''
    return a * b


print(multiply.name)
print(multiply.description)
print(multiply.args)
