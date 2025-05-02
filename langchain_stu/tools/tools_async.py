# -*- coding: utf-8 -*-
# @Time : 2025/5/2 23:19
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?p=7&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : tools_async.py
# @Software: PyCharm 
# @Comment :
from langchain_core.tools import tool


@tool
async def amultiply(a: int, b: int) -> int:
    ''' multiply two numbers.'''
    return a * b


print(amultiply.name)
print(amultiply.description)
print(amultiply.args)
