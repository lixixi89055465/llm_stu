# -*- coding: utf-8 -*-
# @Time : 2025/5/1 18:16
# @Author : nanji
# @Site : 
# @File : xml_output_parser_stream.py
# @Software: PyCharm 
# @Comment :
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import XMLOutputParser
# 加载环境变量
import os
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
# pip install defusedxml
# pip install -qU langchain langchain-openai
model = ChatOpenAI(model='gpt-4o', temperature=0)
# 还有一个用于提示语言模型填充数据结构的查询意图
actor_query = '生成周星驰的简化电影作品列表，按照最新的时间降序'
# 设置 解析器 + 将指令注入提示模板
parser = XMLOutputParser()
prompt = PromptTemplate(
    template='回答用户的查询。\n{format_instructions}\n{query} \n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()},
)
print(parser.get_format_instructions())

chain = prompt | model | parser
for s in chain.stream({'query': actor_query}):
    print(s)
