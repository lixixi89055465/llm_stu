# -*- coding: utf-8 -*-
# @Time : 2025/6/21 08:52
# @Author : nanji
# @Site : 
# @File : node_case.py
# @Software: PyCharm 
# @Comment : https://www.yuque.com/aaron-wecc3/dhluml/xgvxqva8u9gcuilb
'''
大模型资料链接: https://pan.baidu.com/s/1DArnJhOdpjZv1KGMZAmBPw?pwd=rjsi 提取码: rjsi
https://www.yuque.com/aaron-wecc3/dhluml?#  密码：ghkq

pip install pydantic -U
'''

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END

# 初始化StateGraph,状态累ing字典
graph = StateGraph(dict)


# 定义节点
def my_node(state: dict, config: RunnableConfig):
    print('In node:', config['configurable']['user_id'])
    return {'results': f'hello ,{state["input"]}!'}


def my_other_node(state: dict):
    return state


# 讲节点添加到图中
graph.add_node('my_node', my_node)
graph.add_node('other_node', my_other_node)
# 🔗3节点以确保它们是科大的
graph.add_edge(START, 'my_node')
graph.add_edge('my_node', 'other_node')
graph.add_edge('other_node', END)
# 编译图
draw = graph.compile()

graph_png = draw.get_graph().draw_mermaid_png()
with open('node_case.py.png', 'wb') as f:
    f.write(graph_png)
