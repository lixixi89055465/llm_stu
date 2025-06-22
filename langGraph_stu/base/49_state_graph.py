# from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langgraph.graph import START, StateGraph
from langchain_core.messages import HumanMessage


class MyState(TypedDict):
    pass


graph = StateGraph(MyState)


def my_node(state, config):
    return {'x': state['x'] + 1, 'y': state['y'] + 2}


# 创建一个状态图构建器builder,使用字典类型作为状态类型
builder = StateGraph(dict)
# 向构建起重添加节点 myNode,节点名称自动设置为'my_node'
builder.add_node(my_node)
# 添加一条边，从START到'my_node'节点
builder.add_edge(START, 'my_node')

# 编译状态图，生成可执行的图
graph = builder.compile()
# 调用编译后的图，传入初始状态{'x':1}
print(graph.invoke({'x': 1, 'y': 2}))



# 6. 执行图，使用可运行对象
final_state = graph.invoke(
    {'messages': [HumanMessage(content='上海的天气怎么样?')]},
    config={'configurable': {'thread_id': 42}}
)
result = final_state['messages'][-1].content
print(result)

final_state = graph.invoke(
    {'messages': [HumanMessage(content='我问的那个城市?')]},
    config={'configurable': {'thread_id': 42}}
)

# 将生成的图片保存到文件
graph_png = graph.get_graph().draw_mermaid_png()
with open('49_state_graph.py.png', 'wb') as f:
    f.write(graph_png)
