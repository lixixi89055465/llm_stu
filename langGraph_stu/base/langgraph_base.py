# -*- coding: utf-8 -*-
# @Time : 2025/6/17 20:44
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1boTxzREoH/?spm_id_from=333.1391.0.0&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : langgraph_base.py
# @Software: PyCharm 
# @Comment :

from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
# pip install -U langgraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode


# 定义 工具函数，用于嗲里调用外部工具
@tool
def search(query: str):
    '''模拟一个搜索工具'''
    if '上海' in query.lower() or 'Shanghai' in query.lower():
        return '现在 30度，有雾'
    return '现在是 35度，阳光明媚'


# 将工具函数放入工具列表
tools = [search]
# 创建工具节点
tool_node = ToolNode(tools)
# 1.初始化模型和工具，定义并绑定工具到模型
# model = ChatOpenAI(model='gpt-4o', temperature=0).bind_tools(tools)
base_url = "http://192.168.11.178:11434/v1"
model = ChatOpenAI(base_url=base_url, api_key='empty', model='qwen2:latest', temperature=0).bind_tools(tools)


# 定义函数，定义并绑定工具到模型
def should_continue(state: MessagesState) -> Literal['tools', END]:
    messages = state['messages']
    last_message = messages[-1]
    # 如果 LLM 调用了工具，则转到 'tools'节点
    if last_message.tool_calls:
        return 'tools'
    # 否则，停止（回复用户)
    return END


# 定义调用模型的函数
def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    # 返回列表，因为这将被添加到现有列表中
    return {'messages': [response]}


# 2 .用状态初始化图，定义一个新的状态图
workflow = StateGraph(MessagesState)
# 3.定义图节点，定义我们将循环的两个节点
workflow.add_node('agent', call_model)
workflow.add_node('tools', tool_node)

# 4.定义入口点和图边
# 设置入口点为'agent'
# 这意味着这是第一个被调用的节点
workflow.set_entry_point('agent')
# 添加条件边
workflow.add_conditional_edges(
    # 首先，定义起始节点。我们使用 'agent'.
    # 这意味着这些边是在调用'agent'节点后采取的。
    'agent',
    # 接下来，传遍决定下一个调用节点的函数。
    should_continue
)
# 添加 聪'tools'到’agent'的普通边。
# 这意味着在调用'tools'后，接下来调用'agent'节点 .
workflow.add_edge('tools', 'agent')
# 初始化内存已在图运行之间持久化状态
checkpointer = MemorySaver()
# 5.编译图
# 这讲起编译成 一个 LangChain可运行对象
# 这意味着可以使用其他客运行对象一样使用它.
# 注意，我们（可选地（在编译图时 传递内存
app = workflow.compile(checkpointer=checkpointer)
# 6. 执行图，使用可运行对象
final_state = app.invoke(
    {'messages': [HumanMessage(content='上海的天气怎么样?')]},
    config={'configurable': {'thread_id': 42}}
)

result = final_state['messages'][-1].content
print(result)

# 将生成的图片保存到文件
graph_png = app.get_graph().draw_mermaid_png()
with open('langgraph_base.png', 'wb') as f:
    f.write(graph_png)
