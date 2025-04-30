# -*- coding: utf-8 -*-
# @Time : 2025/4/30 17:40
# @Author : nanji
# @Site : 
# @File : testTool01.py
# @Software: PyCharm 
# @Comment :

from langchain.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


print(multiply.name)
print(multiply.description)
print(multiply.args)

res = multiply.run({'a': 10, 'b': 20})
print(res)
