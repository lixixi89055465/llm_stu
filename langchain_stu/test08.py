# -*- coding: utf-8 -*-
# @Time : 2025/4/24 21:33
# @Author : nanji
# @Site : 
# @File : test08.py
# @Software: PyCharm 
# @Comment :
LANGSMITH_TRACING = True
LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"
LANGSMITH_API_KEY = "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"
LANGSMITH_PROJECT = "pr-only-platinum-89"
OPENAI_API_KEY = "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"
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm.invoke("Hello, world!")