# -*- coding: utf-8 -*-
# @Time : 2025/4/30 22:35
# @Author : nanji
# @Site : 
# @File : json_output_parser_no_pydantic.py
# @Software: PyCharm 
# @Comment :
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
# 加载环境变量
import os
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'

model = ChatOpenAI(model='gpt-4o', temperature=0)
joke_query = '告诉我一个笑话'
parser = JsonOutputParser()
prompt = PromptTemplate(
    template='A回答用户的查询。\n{format_instructions} \n {query}\n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)
chain = prompt | model | parser
response = chain.invoke({'query': joke_query})
print(response)

# {'response': '为什么数学书总是很忧郁？因为它有太多的问题！'}

