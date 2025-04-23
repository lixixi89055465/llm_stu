# -*- coding: utf-8 -*-
# @Time : 2025/4/21 22:31
# @Author : nanji
# @Site : 
# @File : llm_app.py
# @Software: PyCharm 
# @Comment :
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
# 加载 环境变量
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(
    find_dotenv(),
    verbose=True  # 读取本地.env 文件，里面定义了OPENAI_API_KEY
)

# 引入langchain openai sdk
llm=ChatOpenAI()


# 根据 message生成提示词模板
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是世界级的技术专家'),
    ('user', '{input}')
])
# 通过langchain的链式调用
chain = prompt | llm

result=chain.invoke({'input':'帮我写一篇关于 AI　的技术文章，100个字'})
print(result)