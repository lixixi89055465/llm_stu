# -*- coding: utf-8 -*-
# @Time : 2025/5/1 9:26
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?spm_id_from=333.1391.0.0&p=6&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : xml_output_parser.py
# @Software: PyCharm
# @Comment :

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import XMLOutputParser
from langchain.output_parsers.yaml import YamlOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field

# 加载环境变量
import os

os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
# pip install defusedxml
# pip install -qU langchain langchain-openai
model = ChatOpenAI(temperature=0)


# 还有一个用于提示语言模型填充数据结构的查询意图
# 定义您期望的数据结构
class Joke(BaseModel):
    setup: str = Field(description='设置笑话的问题')
    punchline: str = Field(description='解决笑话的答案')


actor_query = '告诉我一个笑话'
# 设置 解析器 + 将指令注入提示模板
parser = YamlOutputParser(pydantic_object=Joke)
prompt = PromptTemplate(
    template='回答用户的查询。\n{format_instructions}\n{query} \n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()},
)
print(parser.get_format_instructions())
chain = prompt | model
response = chain.invoke({'query': actor_query})
xml_output = parser.parse(response.content)
print(response.content)
'''
The output should be formatted as a YAML instance that conforms to the given JSON schema below.

# Examples
## Schema
```
{"title": "Players", "description": "A list of players", "type": "array", "items": {"$ref": "#/definitions/Player"}, "definitions": {"Player": {"title": "Player", "type": "object", "properties": {"name": {"title": "Name", "description": "Player name", "type": "string"}, "avg": {"title": "Avg", "description": "Batting average", "type": "number"}}, "required": ["name", "avg"]}}}
```
## Well formatted instance
```
- name: John Doe
  avg: 0.3
- name: Jane Maxfield
  avg: 1.4
```

## Schema
```
{"properties": {"habit": { "description": "A common daily habit", "type": "string" }, "sustainable_alternative": { "description": "An environmentally friendly alternative to the habit", "type": "string"}}, "required": ["habit", "sustainable_alternative"]}
```
## Well formatted instance
```
habit: Using disposable water bottles for daily hydration.
sustainable_alternative: Switch to a reusable water bottle to reduce plastic waste and decrease your environmental footprint.
``` 

Please follow the standard YAML formatting conventions with an indent of 2 spaces and make sure that the data types adhere strictly to the following JSON schema: 
```
{"properties": {"setup": {"description": "\u8bbe\u7f6e\u7b11\u8bdd\u7684\u95ee\u9898", "title": "Setup", "type": "string"}, "punchline": {"description": "\u89e3\u51b3\u7b11\u8bdd\u7684\u7b54\u6848", "title": "Punchline", "type": "string"}}, "required": ["setup", "punchline"]}
```

Make sure to always enclose the YAML output in triple backticks (```). Please do not add anything other than valid YAML output!
```
setup: 为什么海洋总是蓝色的？
punchline: 因为鱼在水里每次见到海洋都在说"嗨，蓝！"
```
'''
