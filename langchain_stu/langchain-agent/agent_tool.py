# -*- coding: utf-8 -*-
# @Time : 2025/6/9 21:43
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1Ro3ze4EX4?t=916.8
# @File : test_agent.py
# @Software: PyCharm 
# @Comment :
'''
pip install google-search-results
pip install numexpr
'''
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, Tool

from langchain_community.agent_toolkits.load_tools import load_tools
import os
# 加载环境变量
import os

# os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
# os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
# api_key = os.environ['OPENAI_API_KEY']
# os.environ['SERPAPI_API_KEY']=''
os.environ["SERPAPI_API_KEY"] = "d4dd7f852c4a8468fe1468814b56ad7f11af487c013b1cee8c1f74c2289c0835"


def sum(string):
    x = int(string.split(',')[0])
    y = int(string.split(',')[1])
    return x + y


# os.environb[''] = '1'
base_url = "http://192.168.11.178:11434/v1"

sum_fun = Tool.from_function(
    func=sum,
    name='sum',
    description='这是一个智慧做加法运算的 计算器，当用户需要得到两个数的和时，请调用 su没方法让进行加法运算，'
                '并且两个参数之间用逗号隔开，并返回运算后的结果'
)
llm = ChatOpenAI(
    # model='gpt-4o',
    # model='chevalblanc/gpt-4o-mini:latest',
    model='qwen2:latest',
    temperature=0,
    api_key='fdsfadfsaf', base_url=base_url
)
# tools = load_tools(['serpapi', 'dalle-image-generator', 'llm-math'], llm=llm)
tools = load_tools(['serpapi', 'llm-math'], llm=llm)
# tools = load_tools(['serpapi' ], llm=llm)
# tools.append(sum_fun)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
# res = agent.run('请按照北京的时区告诉我今天是星期几，几月几号')
# res = agent.run('请帮我生成两张关于北京风景的图片')
res = agent.run('请帮我计算 8*8*8等于几')
print(res)
