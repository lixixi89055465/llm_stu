# -*- coding: utf-8 -*-
# @Time : 2025/4/23 22:45
# @Author : nanji
# @Site : 
# @File : stream_llm.py
# @Software: PyCharm 
# @Comment :
from langchain_openai import ChatOpenAI


# 加载 环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(
    find_dotenv(),
    verbose=True  # 读取本地.env 文件，里面定义了OPENAI_API_KEY
)

model = ChatOpenAI(model='gpt-4')

chunks = []
for chunk in model.stream('天空是什么颜色的?'):
    chunks.append(chunk)
    print(chunk.content, end='|', flush=True)
