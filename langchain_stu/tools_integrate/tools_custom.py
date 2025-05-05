# -*- coding: utf-8 -*-
# @Time : 2025/5/4 22:40
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9?t=1429.9&p=7
# @File : tools_custom.py
# @Software: PyCharm 
# @Comment :
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field

# api_wrapper=WikipediaAPIWrapper(top)
api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=100
)


class WikiInputs(BaseModel):
    ''' 维基百科工具的输入。'''
    query: str = Field(
        description='query to look up in Wikipedia, should be 3 or less words'
    )


tool = WikipediaQueryRun(
    name='wiki-tool',
    description='look up things in wikipedia',
    args_schema=WikiInputs,
    api_wrapper=api_wrapper,
    # 如果return_direct 设置为True,工具会直接返回查询结果。例如，一个字符串或ige简单的数据结构
    # 如果return_direct 设置为False,工具可能返回一个更复杂的相应对象，其中包括更多的元数据后结构化信息
    return_direct=True,
)
