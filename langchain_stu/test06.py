# -*- coding: utf-8 -*-
# @Time : 2025/4/24 17:37
# @Author : nanji
# @Site : https://blog.csdn.net/shuz0612/article/details/145761831
# @File : test06.py
# @Software: PyCharm 
# @Comment :

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位IT技术专家。回答问题时准确且简洁。"),
        MessagesPlaceholder("history"),
        ("human", "{question}")
    ]
)

model = ChatOllama(model="qwen2.5:3b")
chain = prompt | model | StrOutputParser()
response = chain.invoke({
    "history": [("human", "介绍下LLM"), ("ai", "LLM即大型语言模型，基于深度学习技术，能对语意进行理解。")],
    "question": "介绍LLM的一个核心技术点"})
print(response)
