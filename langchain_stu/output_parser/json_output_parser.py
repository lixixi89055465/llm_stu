# -*- coding: utf-8 -*-
# @Time : 2025/4/30 22:13
# @Author : nanji
# @Site : 
# @File : json_output_parser.py
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
    setup: str = Field(description='设置笑话的问题 ')
    punchline: str = Field(description='解决笑话的答案')


# 还有一个用于提示语言模型填充数据结构的查询意图
joke_query = '告诉我一个笑话.'
# 设置解析器 + 将指令注入提示模板
parser = JsonOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template='回答用户的查询.\n {format_instructions} \n {query}\n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)
print(parser.get_format_instructions())
chain = prompt | model | parser
response = chain.invoke({'query': joke_query})
print(response)

# The output should be formatted as a JSON instance that conforms to the JSON schema below.
#
# As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
# the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.
#
# Here is the output schema:
# ```
# {"properties": {"setup": {"title": "Setup", "description": "设置笑话的问题 ", "type": "string"}, "punchline": {"title": "Punchline", "description": "解决笑话的答案", "type": "string"}}, "required": ["setup", "punchline"]}
# ```
# {'setup': '为什么橙子在学校表现得如此糟糕？', 'punchline': '因为它总是被果汁（拘束）！'}

