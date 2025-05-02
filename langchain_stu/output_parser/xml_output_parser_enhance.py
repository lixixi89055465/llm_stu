# -*- coding: utf-8 -*-
# @Time : 2025/5/1 18:06
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?p=6&spm_id_from=333.788.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : xml_output_parser_enhance.py
# @Software: PyCharm 
# @Comment :
from langchain_openai import ChatOpenAI
# pip install -qU langchain langchain_openai
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import XMLOutputParser
# 加载环境变量
import os
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
# pip install defusedxml

model = ChatOpenAI(model='gpt-4o', temperature=0)

# 还有一个用于提示语言模型填充数据结构的查询意图
actor_query = '生成周星驰的简化电影作品列表，按照最新的时间降序'
# 设置解析器 + 将指令注入提示模板
parser = XMLOutputParser(tags=['movies', 'actor', 'film', 'name', 'genre'])
prompt = PromptTemplate(
    template='回答用户的查询。\n{format_instructions}\n {query}\n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)
print(parser.get_format_instructions())
chain = prompt | model
response = chain.invoke({'query': actor_query})
xml_output = parser.parse(response.content)
print(response.content)

'''

The output should be formatted as a XML file.
1. Output should conform to the tags below.
2. If tags are not given, make them on your own.
3. Remember to always open and close all the tags.

As an example, for the tags ["foo", "bar", "baz"]:
1. String "<foo>
   <bar>
      <baz></baz>
   </bar>
</foo>" is a well-formatted instance of the schema.
2. String "<foo>
   <bar>
   </foo>" is a badly-formatted instance.
3. String "<foo>
   <tag>
   </tag>
</foo>" is a badly-formatted instance.

Here are the output tags:
```
['movies', 'actor', 'film', 'name', 'genre']
```
```xml
<movies>
    <actor>
        <name>周星驰</name>
        <film>
            <name>美人鱼</name>
            <genre>喜剧, 奇幻</genre>
        </film>
        <film>
            <name>西游·降魔篇</name>
            <genre>喜剧, 奇幻</genre>
        </film>
        <film>
            <name>长江7号</name>
            <genre>喜剧, 科幻</genre>
        </film>
        <film>
            <name>功夫</name>
            <genre>喜剧, 动作</genre>
        </film>
        <film>
            <name>少林足球</name>
            <genre>喜剧, 体育</genre>
        </film>
    </actor>
</movies>
```
'''