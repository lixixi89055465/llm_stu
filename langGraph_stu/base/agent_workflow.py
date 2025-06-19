# -*- coding: utf-8 -*-
# @Time : 2025/6/18 21:24
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1boTxzREoH?t=1147.0&p=2
# @File : agent_workflow.py
# @Software: PyCharm 
# @Comment : python=3.12
import os
from typing import Literal
from langgraph.graph import END, StateGraph, MessagesState

os.environ['TAVILY_API_KEY'] = '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'

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'

# 导入 langchain 的 hub哭和 ChatOpenAI类，以及 asyncio
from langchain import hub
from langchain_openai import ChatOpenAI

# 执行 asyncio哭的 run_until
import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults

# 创建 TavilySearchresults 工具，设置最大结果数是 1
tools = [TavilySearchResults(max_results=1)]

# 聪 LangChain的 hubzhong 获取 prompt模板，可以进行修改
prompt = hub.pull('wfh/react-agent-executor')
prompt.pretty_print()
# 选择驱动代理的 LLM，使用 OpenAI 的 chatGPT-4o 模型
# llm = ChatOpenAI(model='gpt-4o')
base_url = "http://192.168.11.178:11434/v1"
llm = ChatOpenAI(base_url=base_url, api_key='empty',
                 model='qwen2:latest',
                 temperature=0).bind_tools(tools)
# model = ChatOpenAI(model='gpt-4o', temperature=0).bind_tools(tools)


# 创建一个 REACT 代理执行器，使用只能怪的 LLM 和工具，并应用聪 hub中获取的 prompt
agent_executor = create_react_agent(llm, tools, state_modifier=prompt)
# 调用代理执行器，询问"谁是美国公开赛的冠军"
# agent_executor.invoke({'messages': [('user', '谁是美国公开赛的获胜者')]})
import operator
from typing import Annotated, List, Tuple, TypedDict


# 定义一个 TypeDict类 PlanExecute,用于存储输入，计划，过去的步骤和相应
class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str


from pydantic import BaseModel, Field


# 定义一个 Planmoxinglei ,用于描述未来要执行的计划
class Plan(BaseModel):
    '''未来要执行的计划 '''
    steps: List[str] = Field(
        description='需要执行的不同步骤，应该按照顺序排列 '
    )


from langchain_core.prompts import ChatPromptTemplate

# 创建一个计划生成的提示模板
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '''
     对于给定的目标，提出一个简单的逐步计划。这个计划应该包含独立的任务，
     如果正确执行将得出正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。
     确保每一步都有所有必要的信息 - 不要跳过步骤。
            '''
        ),
        ('placeholder', '{messages}')
    ]
)
# 使用指定的提示模版创建一个计划生成器，使用 openaide ChatGPT-4o模型
planner = planner_prompt | ChatOpenAI(base_url=base_url,
                                      api_key='empty',
                                      model='qwen2:latest',
                                      temperature=0).with_structured_output(Plan)
# 调用家护色很长期，寻味“当前安达里呀公开赛冠军的家乡是哪里？
planner.invoke({'messages': [('user', '现任澳网冠军的家乡是哪里?')]})
from typing import Union


# 定义一个相应模型类，用于描述哦你过户的相应
class Response(BaseModel):
    '''用户相应'''
    response: str


# 定义一个行为模型类，用于描述要执行的行为
class Act(BaseModel):
    '''要执行的行为 '''
    action: Union[Response, Plan] = Field(
        description='要执行的行为。如果要回应用户，使用Response。如果需要进一步使用工具获取答案，使用Plan。'
    )


# 创建一个重新计划的提示模板
replanner_prompt = ChatPromptTemplate.from_template(
    """对于给定的目标，提出一个简单的逐步计划。这个计划应该包含独立的任务，
    如果正确执行将得出正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。
    确保每一步都有所有必要的信息 - 不要跳过步骤。
    你的目标是：
    {input}
   你的原计划是： 
   {plan} 
   你目前已完成的步骤是： 
   {past_steps}
   相应地更新你的计划。如果不需要更多步骤并且可以返回给用户，那么就这样回应。如果需要，填写计划。
   只添加仍然需要完成的步骤。不要返回已完成的步骤作为计划的一部分。
    """
)
# replanner = replanner_prompt | ChatOpenAI(
#     model='gpt-4o', temperature=0
# ).with_structured_output(Act)
replanner = replanner_prompt | ChatOpenAI(
    base_url=base_url,
    api_key='empty',
    model='qwen2:latest', temperature=0
).with_structured_output(Act)
# 使用指定的提示模板创建一个重新计划生成器，使用 OpenAI ChatGPT-4o模型
from langgraph.graph import StateGraph, START


# 使用指定的提示模板创建一个重新计划生成器，使用OpenAI的ChatGPT-4o模型
async def main():
    # 定义一个异步函数，用于生成计划步骤
    async def plan_step(state: PlanExecute):
        plan = await planner.ainvoke({'messages': [('user', state['input'])]})
        return {'plan': plan.steps}

    # 定义一个异步函数，用于执行步骤
    async def execute_step(state: PlanExecute):
        plan = state['plan']
        plan_str = '\n'.join(f'{i + 1},{step}' for i, step in enumerate(plan))
        task = plan[0]
        task_formatted = f'''
        对于一下计划:
        {plan_str}\n\n你的任务执行第{1}步，{task},'''
        agent_response = await agent_executor.ainvoke(
            {'messages': [('user', task_formatted)]}
        )
        return {
            'past_steps': state['past_steps'] + [(task, agent_response['messages'][-1].content)]
        }

    # 定义一个函数，用于判断是否结束
    async def replan_step(state: PlanExecute):
        output = await replanner.ainvoke(state)
        if isinstance(output.action, Response):
            return {'response': output.action.response}
        else:
            return {'plan': output.action.steps}

    def should_end(state: PlanExecute) -> Literal['agent', '__end__']:
        if 'response' in state and state['response']:
            return '__end__'
        else:
            return 'agent'

    # 创建一个状态图 ,初始化 PlanExecute
    workflow = StateGraph(PlanExecute)
    # 添加计划节点
    workflow.add_node('planner', plan_step)
    # 添加执行步骤节点
    workflow.add_node('agent', execute_step)
    # 添加重新计划节点
    workflow.add_node('replan', replan_step)
    # 设置聪开始到计划节点的变
    workflow.add_edge(START, 'planner')
    # 设置从计划到代理节点的变
    workflow.add_edge('planner', 'agent')
    # 设置聪代理到重新计划节点的变
    workflow.add_edge('agent', 'replan')
    # 添加条件边，用于判断下一步操作
    workflow.add_conditional_edges(
        'replan',
        # 传入判断函数，确定下一个节点
        should_end
    )
    # 变异状态图，生成 LangChain可运行对象
    app = workflow.compile()
    # 将生成的图片保存到文件
    graph_png = app.get_graph().draw_mermaid_png()
    with open('plan_execute.png', 'wb') as f:
        f.write(graph_png)
