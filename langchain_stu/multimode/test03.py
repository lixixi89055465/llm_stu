# -*- coding: utf-8 -*-
# @Time : 2025/4/30 18:38
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9?spm_id_from=333.788.player.switch&vd_source=50305204d8a1be81f31d861b12d4d5cf&p=6
# @File : test03.py
# @Software: PyCharm 
# @Comment :
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel,Field
from langchain_openai import ChatOpenAI

model=ChatOpenAI(model='gpt-4o',temperature=0)

# 定义您期望的数据结构
class Joke(BaseModel):
    setup:str=Field(description='设置笑话的问题')
    punchline:str=Field(description='解决笑话的答案')

# 还有一个用于提示语言模型填充数据结构的查询意图


