# -*- coding: utf-8 -*-
# @Time : 2025/6/11 20:32
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1rohGe3EV7/?spm_id_from=333.1387.upload.video_card.click
# @File : test_server.py
# @Software: PyCharm 
# @Comment :
import uvicorn
from fastapi import FastAPI
from flask import Flask
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentType, initialize_agent, Tool

# from flask_api.project.config import OPENAI_BASE_URL
OPENAI_BASE_URL = ''

app = FastAPI()
import os

os.environ['OPEN_API_BASE'] = OPENAI_BASE_URL
os.environ['OPEN_API_KEY'] = 'empty'
os.environ["SERPAPI_API_KEY"] = "d4dd7f852c4a8468fe1468814b56ad7f11af487c013b1cee8c1f74c2289c0835"

base_url = "http://192.168.11.178:11434/v1"


class aiAssistant:
    def __init__(self):
        self.chatmodel = ChatOpenAI(
            # model='Qwen2-14B-merge-GPTQ-Int8',
            model='qwen2:latest',
            temperature=0,
            api_key='fdasfs',
            base_url=base_url
        )
        self.memory_key = 'chat_history'
        self.prompt = ChatPromptTemplate.from_messages(
            [('system', '你是一个智能助手'),
             ('human', '{input}'),
             MessagesPlaceholder(variable_name='agent_scratchpad')]
        )
        self.memory = ''
        self.tools = load_tools(['serpapi'])
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.chatmodel,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def run_agent(self, query):
        res = self.agent.invoke(input=query)
        return res


# if __name__ == '__main__':
#     ai = aiAssistant()
#     # res = ai.run_agent('上海今天天气如何')
#     res = ai.run_agent('请按照中国所在的时区告诉我，今天星期几')
#     print(res)


#
@app.get('/')
def hello_world():
    return {'message': 'hello world'}


@app.get('/chat')
def chat(query):
    # return {'message': 'hello world1111'}
    ai = aiAssistant()
    res = ai.run_agent(query)
    return res['output']


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
