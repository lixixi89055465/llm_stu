# -*- coding: utf-8 -*-
# @Time : 2025/5/3 21:23
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?p=7&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : structured_tools.py
# @Software: PyCharm 
# @Comment :

from langchain_core.tools import StructuredTool
import asyncio


def multiply(a: int, b: int) -> int:
    '''multiply two numbers.'''
    return a * b


async def amultiply(a: int, b: int) -> int:
    ''' Multiply two numbers. '''
    return a * b


async def main():
    # func 参数 ：指定一个同步函数。当你再同步上下文中调用工具时，它会使用这个同步函数来执行操作。
    # oroutine 参数：指定一个异步函数。当你再异步上下文中调用工具时，它会使用这个异步函数来指定操作。
    calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)
    # invoke 是同步调用
    print(await calculator.ainvoke({'a': 2, 'b': 5}))
    # ainvoke 是异步调用
    print(calculator.invoke({'a': 2, 'b': 3}))


# 运行异步主函数
asyncio.run(main())
