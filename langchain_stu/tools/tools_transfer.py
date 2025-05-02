# -*- coding: utf-8 -*-
# @Time : 2025/5/2 22:56
# @Author : nanji
# @Site : 
# @File : tools_transfer.py
# @Software: PyCharm 
# @Comment :

# 导入工具装饰器库
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description='first number')
    b: int = Field(description='second number')


@tool('multiplication-tool', args_schema=CalculatorInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    '''multiply two numbers.'''
    return a * b




# 让我们检查与该工具关联的一些属性
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)
print(multiply.invoke({'a': 2, 'b': 3}))

'''
multiplication-tool
multiply two numbers.
{'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}
True
6
'''