# -*- coding: utf-8 -*-
# @Time : 2025/6/13 21:46
# @Author : nanji
# @Site :https://www.bilibili.com/video/BV1uS421R7yq?t=751.1
# @File : graph_test.py
# @Software: PyCharm 
# @Comment :
import time
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
# from langgraph.checkpoint import MemoryServer
# from langgraph.checkpoint import MemorySaver
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from langGraph_stu.tools import RagTool, createAccount, createOrder, bingAccountOrder

import os
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'


class langGraphLearn(object):
    def __init__(self):
        self.tools = [RagTool(), createOrder(), createAccount(), bingAccountOrder()]
        self.tool_node = ToolNode(self.tools)
        self.model = ChatOpenAI(temperature=0, model='gpt-4o').bind_tools(self.tools)

    def should_continue(self, state: MessagesState) -> Literal['tools', END]:
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return 'tools'
        return END

    def call_model(self, state: MessagesState):
        messages = state['messages']
        response = self.model.invoke(messages)
        return {'messages': [response]}

    def run_langgraph(self):
        workflow = StateGraph(MessagesState)
        workflow.add_node('agent', self.call_model)
        workflow.add_node('tools', self.tool_node)
        workflow.set_entry_point('agent')
        workflow.add_conditional_edges(
            'agent', self.should_continue
        )
        workflow.add_edge('tools', 'agent')
        checkpointer = MemorySaver()
        app = workflow.compile(checkpointer=checkpointer)
        messages = [
            SystemMessage(
                content='你是一位智能客服，通过调用工具来对用户进行问答,请使用原文回答，'
                        '不需要对用户进行解释。'
            )
        ]
        while True:
            human = input('请输入你的问题:')
            start_time = time.time()
            messages.append(HumanMessage(content=human))
            final_state = app.invoke(
                {'messages': messages},
                config={'configurable': {'thread_id': 42}}
            )
            messages.append(AIMessage(content=final_state['messages'][-1].content))
            print(final_state['messages'][-1].content)
            print('总耗时:', time.time() - start_time)


if __name__ == '__main__':
    print('aaa')
