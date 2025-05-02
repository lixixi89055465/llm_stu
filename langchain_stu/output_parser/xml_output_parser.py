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
None
```
```xml
<周星驰电影作品>
    <电影>
        <名称>新喜剧之王</名称>
        <年份>2019</年份>
    </电影>
    <电影>
        <名称>美人鱼</名称>
        <年份>2016</年份>
    </电影>
    <电影>
        <名称>西游降魔篇</名称>
        <年份>2013</年份>
    </电影>
    <电影>
        <名称>长江七号</名称>
        <年份>2008</年份>
    </电影>
    <电影>
        <名称>功夫</名称>
        <年份>2004</年份>
    </电影>
    <电影>
        <名称>少林足球</名称>
        <年份>2001</年份>
    </电影>
    <电影>
        <名称>喜剧之王</名称>
        <年份>1999</年份>
    </电影>
    <电影>
        <名称>大内密探零零发</名称>
        <年份>1996</年份>
    </电影>
    <电影>
        <名称>国产凌凌漆</名称>
        <年份>1994</年份>
    </电影>
    <电影>
        <名称>破坏之王</名称>
        <年份>1994</年份>
    </电影>
</周星驰电影作品>
```
'''