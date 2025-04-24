# -*- coding: utf-8 -*-
# @Time : 2025/4/24 21:30
# @Author : nanji
# @Site : 
# @File : test07.py
# @Software: PyCharm 
# @Comment :

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Tongyi
from langserve import add_routes
import os

os.environ["DASHSCOPE_API_KEY"] = "你的API_KEY"

# 1. 创建提示词模版
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. 创建模型
model = Tongyi()

# 3. 创建解析器
parser = StrOutputParser()

# 4. 创建链
chain = prompt_template | model | parser