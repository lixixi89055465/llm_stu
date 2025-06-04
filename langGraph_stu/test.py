# -*- coding: utf-8 -*-
# @Time : 2025/5/28 21:54
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1bEh1ejEnn?t=672.3
# @File : test.py
# @Software: PyCharm
# @Comment :
'''
langChain有个 agent,通过用户的一些输入或者 prompt来调用一些工具，比如搜索，或者调用 api,他会能够对
用户提出的任务进行一个编排，问某某人的老公/老婆，主持过什么节目
先搜索这个人的老婆/老公是谁，再去搜索主持过什么节目
先定一一个搜索功能的 tool agent 去做任务编排再通过任务调用对应tool来得到答案

langraph
state  状态 --用来判断是否进行调用工具还是结束调用
node     点  --封装一个 tool,大模型
edge    线   --通过 tool 指向大模型 或者 tool 指向另外一个 tool 也可以是大模型指向 tool
graph   图   --所有线   组成的就是图

状态转换，每次执行完一个 node之后，判断 是否需要调用其他 node,如果调用其他 node,
则状态设置为调用其他 node,否则将状态设置为结束
'''
import os
from typing import Literal, Type, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langgraph.prebuilt import ToolNode
import os

os.environ["OPENAI_API_BASE"] = "https://api.fe8.cn/v1"
os.environ["OPENAI_API_KEY"] = "sk-KtPNRHP3PqYA7adlrr3JcaNwsuv5jnnDsshW6vT1NQ6rVBZa"


class createCarInput(BaseModel):
    a: str = Field(..., description='发动机')
    b: str = Field(..., description='底盘')
    c: str = Field(..., description='变速箱')


class createCar(BaseTool):
    name = 'createCar'
    description = '''
                  这是一个生成车信息的方法，需要用户提供发动机，底盘，变速箱信息才能进行造车，
                   如果用户没有提供这些信息，或者缺少一些信息，
                   则提示用户提供对应的信息指导需要的信息完整，才能进行造车，并把造车的信息返回给用户
    '''
    args_schema: Type[BaseModel] = "xxx"

    def _run(self, a: str, b: str, c: str) -> str:
        print("调用同步造车的方法")
        return a + b + c

    async def _arun(self, a: str, b: str, c: str) -> str:
        print('调用异步造车的方法')
        return a + b + c


class createAccountInput(BaseModel):
    a: str = Field(..., description="账号名称")


class createAccount(BaseTool):
    name = 'createAccount'
    description = '''
                  这是一个生成账号信息的方法，需要用户提供账号名称，才能进行账号的创建。
                   如果 用户没有提供账号名称，则提示用户给出账号名称并再进行账号的创建。 '''
    arg_schema: Type[BaseModel] = createAccountInput

    def _run(self, a: str) -> str:
        print('调用同步账号信息的方法')
        return a

    async def _arun(self, a: str) -> str:
        print('调用异步账号信息的方法')
        return a


class bingCarAccountInput(BaseModel):
    a: str = Field(..., description='账号名称')
    b: str = Field(..., description='车信息')


class bingCarAccount(BaseTool):
    name = 'bingCarAccount'
    description = ('这是一个绑定账号和车信息的方法，需要用户提供账号名称和车信息，才能进行账号和车信息的绑定，'
                   '如果用户没有提供账号名称或车信息，则提示用户给出账号名称和车信息'
                   '并再进行账号和车信息的绑定。不能单独使用用户提示')
    args_schema: Type[BaseModel] = bingCarAccountInput

    def _run(self, a: str, b: str) -> str:
        print('调用同步账号和车信息绑定的方法')
        return a + b

    async def _arun(self, a: str, b: str) -> str:
        print('调用异步账号和车信息绑定的方法')
        return a + b


tools = [createCar(), createAccount(), bingCarAccount()]
tool_node = ToolNode(tools)
# model = ChatOpenAI(temperature=0, model='gpt-4o').bind_tools(tools)
model = ChatOpenAI(temperature=0, model='gpt-4o')


def should_continue(state: MessagesState) -> Literal['tools', END]:
    '''
    判断是否需要调用工具，如果调用工具，则返回 tools,否则返回END
    '''
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return 'tools'
    return END


def call_model(state: MessagesState) -> MessagesState:
    '''
    调用大模型
    '''
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': [response]}


workflow = StateGraph(MessagesState)

workflow.add_node('agent', call_model)
workflow.add_node('tools', tool_node)

workflow.set_entry_point('agent')

workflow.add_conditional_edges('agent', should_continue)

workflow.add_edge('tools', 'agent')

checkpointer = MemorySaver()

app = workflow.compile(checkpointer=checkpointer)
messages = []
while True:
    user_input = input('请输入:')
    messages.append(HumanMessage(content=user_input))
    response = app.invoke({'messages': messages}, config={'configurable': {"thread_id": 42}})
    # response = app.invoke({'messages': messages})
    messages.append(AIMessage(content=response['messages'][-1].content))
    print(response)
