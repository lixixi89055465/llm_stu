# -*- coding: utf-8 -*-
# @Time : 2025/6/22 15:16
# @Author : nanji
# @Site : https://www.yuque.com/aaron-wecc3/dhluml/nd272e303g00rexv
# @File : breakpoints_case.py
# @Software: PyCharm 
# @Comment :

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display


class State(TypedDict):
    input: str


def step_1(state):
    print('---Step 1-----')
    pass


def step_2(state):
    print('---Step 2-----')
    pass


def step_3(state):
    print('---Step 3-----')
    pass


builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)
builder.add_edge(START, 'step_1')
builder.add_edge('step_1', 'step_2')
builder.add_edge('step_2', 'step_3')
builder.add_edge('step_3', END)
# Set up memory
memory = MemorySaver()
# add
graph = builder.compile(checkpointer=memory, interrupt_before=['step_3'])

# Input
initial_input = {'input': 'hello world'}
# Thread
thread = {'configurable': {"thread_id": "1"}}
# 运行 graph ，知道第一次终端
for event in graph.stream(initial_input, thread, stream_mode='values'):
    print(event)

user_approval = input('Do you want to go to Step 3 ?(yes/no):')
if user_approval.lower() == 'yes':
    # If approved,continue the graph execution
    for event in graph.stream(None, thread, stream_mode='values'):
        print(event)
else:
    print('Operation cancelled by user.')

# 将生成的图片保存到文件
graph_png = graph.get_graph().draw_mermaid_png()
with open('breakpoints_add.py.png', 'wb') as f:
    f.write(graph_png)
