# -*- coding: utf-8 -*-
# @Time : 2025/6/9 21:43
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1TN3weBEBr?t=965.9
# @File : test_agent.py
# @Software: PyCharm 
# @Comment :
'''
pip install google-search-results
pip install numexpr
'''
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent

from langchain_community.agent_toolkits.load_tools import load_tools
import os

# os.environ['SERPAPI_API_KEY']=''
os.environ["SERPAPI_API_KEY"] = "d4dd7f852c4a8468fe1468814b56ad7f11af487c013b1cee8c1f74c2289c0835"

# os.environb[''] = '1'
base_url = "http://192.168.11.178:11434/v1"

llm = ChatOpenAI(
    # model='gpt-4o',
    # model='chevalblanc/gpt-4o-mini:latest',
    model='qwen2:latest',
    temperature=0,
    api_key='3536364636',
    base_url=base_url
)
# res = llm.stream('今天星期几?')
# for i in res:
#     print(i.content, end='', flush=True)
res = llm.invoke('请告诉我今天上海的天气怎么样？')
print(res.content)

tools = load_tools(['serpapi', 'llm-math'], llm=llm)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
# res = agent.run('今天的日期是几月几号？，并且每个数字相加等于多少?')
# res = agent.run('请告诉我今天是几月几号,今天是今年第几天')
print(res)
