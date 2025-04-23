# -*- coding: utf-8 -*-
# @Time : 2025/4/23 22:49
# @Author : nanji
# @Site : 
# @File : astream_chain.py
# @Software: PyCharm 
# @Comment : 异步嵌入式调用
from langchain_openai import ChatOpenAI
import asyncio
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
# 加载 环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(
    find_dotenv(),
    verbose=True  # 读取本地.env 文件，里面定义了OPENAI_API_KEY
)



prompt = ChatPromptTemplate.from_template(
    '给我将一个关于{topic}的笑话'
)
model = ChatOpenAI(model='gpt-4')
parser = StrOutputParser()
chain = prompt | model | parser


async def async_stream():
    async for chunk in chain.astream({'topic': '鹦鹉'}):
        print(chunk, end='|', flush=True)


# 运行异步流处理
asyncio.run(async_stream())
