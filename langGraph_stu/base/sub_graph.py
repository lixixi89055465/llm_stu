# -*- coding: utf-8 -*-
# @Time : 2025/6/22 21:48
# @Author : nanji
# @Site : https://www.yuque.com/aaron-wecc3/dhluml/afb2a832r9nsheov
# @File : sub_graph.py
# @Software: PyCharm 
# @Comment :
from typing import List, TypedDict, Optional
from langgraph.graph import StateGraph, START, END


# 定义日志的结构
class Logs(TypedDict):
    id: str  # 日志的唯一标志服
    question: str  # 问题文本
    docs: Optional[List]  # 可选的相关文档列表
    answer: str  # 回答文本
    grade: Optional[int]  # 可选的评分
    grader: Optional[str]  # 可选的评分者
    feedback: Optional[str]  # 可选的反馈信息


# 定义故障分析状态的结构
class FailureAnalysisState(TypedDict):
    docs: List[Logs]  # 日志列表
    failures: List[Logs]  # 失败的日志列表
    fa_summary: str  # 故障分析总结


# 获取失败的日志
def get_failures(state):
    docs = state['docs']  # 从状态中获取日志
    failures = [doc for doc in docs if 'grade' in doc]
    return {'failures': failures}  # 返回包含失败日志的字典


# 生成故障分析总结
def generate_summary(state):
    failures = state['failures']  # 从状态中获取失败的日志
    # 添加函数：fa_summary=summarize(failures)
    fa_summary = 'Poor quality retrieval of Chroma documentation. '
    return {'fa_summary': fa_summary}  # 返回包含总结的字典


# 常见故障分析的状态图
fa_builder = StateGraph(FailureAnalysisState)  #
fa_builder.add_node('get_failures', get_failures)  # 添加节点：获取失败的日志
fa_builder.add_node('generate_summary', generate_summary)  # 添加节点：生成总结
fa_builder.add_node(START, 'get_failures')  # 添加边：从开始到获取失败的日志
fa_builder.add_edge('get_failures', 'generate_summary')  # 添加边：从获取失败的日志到生成总结的日志
fa_builder.add_edge('generate_summary', END)  # 添加边：从生成总结到结束


# 定义问题总结状态的结构
class QuestionSummarizationState(TypedDict):
    docs: List[Logs]  # 日志列表
    qs_summary: str  # 问题总结
    report: str  # 总结


# 生成问题总结
def generate_summarize(state):
    docs = state['docs']  # 从状态中获取日志
    # 添加函数：summary=summarize(docs)
    summary = 'Questions focused on usage of ChatOllama and Chroma vector store.'
    return {'qs_summary': summary}  # 返回包含总结的字典


# 发送总结到slack
def send_to_slack(state):
    qs_summary = state['qs_summary']  # 从状态中获取问题总结
    # 添加函数： report=report_generation(qs_summary)
    report = 'foo bar baz'  # 固定的报告内容
    return {'report': report}  # 发挥包含报告的字典
# 创建问题总结的状态图
qs_builder=StateGraph(QuestionSummarizationState)
qs_builder.add_node('generate_summarize', generate_summarize)# 添加 节点：生成总结
qs_builder.add_node('send_to_slack', send_to_slack)# 添加节点：发送到Slack.
qs_builder.add_node('format_report_for_stack',END)# 添加边，从格式化报告到结束

