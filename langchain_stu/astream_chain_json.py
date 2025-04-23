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
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import ChatOpenAI

_ = load_dotenv(
    find_dotenv(),
    verbose=True  # 读取本地.env 文件，里面定义了OPENAI_API_KEY
)
model = ChatOpenAI(model='gpt-4')
chain = (
        model | JsonOutputParser()
)


async def async_stream():
    async for text in chain.astream({
        '以JSON 格式输出法国、西班牙和日本的国家及其人口列表。'
        '使用一个带有“countries”外部键的字典，其中包含国家列表。'
        '每个国家都应该有键`name`和`population`'
    }):
        print(text, flush=True)


# 运行异步流处理
asyncio.run(async_stream())
