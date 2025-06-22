# -*- coding: utf-8 -*-
# @Time : 2025/6/22 15:00
# @Author : nanji
# @Site : https://www.yuque.com/aaron-wecc3/dhluml/nd272e303g00rexv
# @File : 52_interrupt.py
# @Software: PyCharm 
# @Comment :
from langgraph.types import interrupt
from langgraph.graph import END, StateGraph, MessagesState

from typing import Literal
from langgraph.types import interrupt, Command
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
# 加载环境变量
import os
# 定义一个状态该类，包含一个消息列表，消息列表带有 add_messages 注解
class State(TypedDict):
    messages: Annotated[list, add_messages]


def human_approval(state: State) -> Command[Literal['some_node']]:
    is_approved = interrupt(
        {
            'question': '这是正确的吗?',
            'llm_output': state['llm_output']
        }
    )
    if is_approved:
        return Command(goto='some_node')
    else:
        return Command(goto='another_node')
# 将节点添加到图形中的适当位置并连接到相关节点 .