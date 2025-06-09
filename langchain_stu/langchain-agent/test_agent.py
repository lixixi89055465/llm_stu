# -*- coding: utf-8 -*-
# @Time : 2025/6/9 21:43
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1TN3weBEBr?t=965.9
# @File : test_agent.py
# @Software: PyCharm 
# @Comment :

from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent

from langchain_community.agent_toolkits.load_tools import load_tools
import os

# os.environb[''] = '1'
base_url = "http://192.168.11.178:11434/v1"

llm = ChatOpenAI(
    # model='gpt-4o',
    model='chevalblanc/gpt-4o-mini:latest',
    temperature=0.7,
    api_key='3536364636',
    base_url=base_url
)
res = llm.stream('今天星期几?')
for i in res:
    print(i.content, end='', flush=True)
