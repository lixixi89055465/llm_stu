# -*- coding: utf-8 -*-
# @Time : 2025/5/3 22:08
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?p=7&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : structured_tools_config.py
# @Software: PyCharm 
# @Comment :


from langchain_core.tools import StructuredTool
import asyncio
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description='first number')
    b: int = Field(description='second number')


def multiply(a: int, b: int) -> int:
    '''multiply two numbers.'''
    return a * b


async def amultiply(a: int, b: int) -> int:
    ''' Multiply two numbers. '''
    return a * b


async def async_addition(a: int, b: int) -> int:
    ''' Multiply two numbers.'''
    return a + b


from langchain_core.tools import StructuredTool
import asyncio


def multiply(a: int, b: int) -> int:
    '''multiply two numbers.'''
    return a * b


async def amultiply(a: int, b: int) -> int:
    ''' Multiply two numbers. '''
    return a * b


async def main():
    calculator = StructuredTool.from_function(
        func=multiply,
        name='calculator',
        description='multiply numbers',
        args_schema=CalculatorInput,
        return_direct=True,
    )
