# -*- coding: utf-8 -*-
# @Time : 2025/4/30 22:49
# @Author : nanji
# @Site : 
# @File : json_output_parser_stream.py
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


# 定义您期望的数据结构
class Joke(BaseModel):
    setup: str = Field(description='设置笑话的问题')
    punchline: str = Field(description='解决笑话的答案')


# 还有一个用于提示语言模型填充数据结构的查询意图
joke_query = '告诉我一个笑话'
# 设置解析器 + 将指令注入提示模板.
parser = JsonOutputParser(pydantic_object=Joke)
prompt = PromptTemplate(
    template='回答用户的查询,\n {format_instructions} \n {query} \n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)
chain = prompt | model | parser
for s in chain.stream({'query': joke_query}):
    print(s)


# {}
# {'setup': ''}
# {'setup': '为什么'}
# {'setup': '为什么自行'}
# {'setup': '为什么自行车'}
# {'setup': '为什么自行车不能'}
# {'setup': '为什么自行车不能站'}
# {'setup': '为什么自行车不能站立'}
# {'setup': '为什么自行车不能站立？'}
# {'setup': '为什么自行车不能站立？', 'punchline': ''}
# {'setup': '为什么自行车不能站立？', 'punchline': '因为'}
# {'setup': '为什么自行车不能站立？', 'punchline': '因为它'}
# {'setup': '为什么自行车不能站立？', 'punchline': '因为它已经'}
# {'setup': '为什么自行车不能站立？', 'punchline': '因为它已经太'}
# {'setup': '为什么自行车不能站立？', 'punchline': '因为它已经太累'}
# {'setup': '为什么自行车不能站立？', 'punchline': '因为它已经太累了'}
# {'setup': '为什么自行车不能站立？', 'punchline': '因为它已经太累了！'}
