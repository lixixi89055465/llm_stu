# -*- coding: utf-8 -*-
# @Time : 2025/5/5 11:36
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9?t=1552.0&p=7
# @File : toolkit_sqlite.py
# @Software: PyCharm 
# @Comment :
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType

db = SQLDatabase.from_uri('sqlite:///langchain.db')
toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0))
print('1' * 100)
print(toolkit.get_tools())

agent_executor = create_sql_agent(
    llm=ChatOpenAI(temperature=0, model='gpt-4'),
    toolkit=toolkit,
    verbose=False,
    agent_type=AgentType.OPENAI_FUNCTIONS
)
result = agent_executor.invoke('Describe the full_llm_cache table')
print(result)
