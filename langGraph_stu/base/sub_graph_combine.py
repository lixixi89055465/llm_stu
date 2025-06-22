# -*- coding: utf-8 -*-
# @Time : 2025/6/22 22:54
# @Author : nanji
# @Site : https://www.yuque.com/aaron-wecc3/dhluml/afb2a832r9nsheov
# @File : sub_graph_combine.py
# @Software: PyCharm 
# @Comment :
from operator import add
from typing import TypedDict, Annotated, Optional, List, Dict, Any, get_type_hints
from langgraph.graph import StateGraph, START, END


# 定义日志的结构
class Logs(TypedDict):
    id: str  # 日志的唯一标志服
    question: Optional[List]  # 可选的相关文档列表
    docs: Optional[List]
    answer: str  # 回答文本
    grade: Optional[int]  # 可选的评分
    grader: Optional[str]  # 可选的评分者
    feedback: Optional[str]  # 可选的反馈信息


# 定义故障分析的结构
class FailureAnalysisState(TypedDict):
    docs: List[Logs]  # 日志列表
    failures: List[Logs]  # 失败的日志列表
    fa_summary: str  # 故障分析总结


def get_failures(state):
    docs = state['docs']  # 从状态中获取日志
    failures = [doc for doc in docs if 'grade' in doc]  # 筛选出包含评分的日志
    return {'failures': failures}  # 返回包含失败日志的字典


# 生成故障分析总结
def generate_summary(state):
    failures = state['failures']  # 从状态中获取失败的日志
    # 添加函数：fa_summary=summarize(failures)
    fa_summary = 'Poor quality retrieval of Chroma documents'
    return {'fa_summary': fa_summary}  # 返回包含总结的字典


# 创建故障分析的状态图
fa_builder = StateGraph(FailureAnalysisState)
fa_builder.add_node('get_failures', get_failures)  # 添加节点：获取失败的日记
fa_builder.add_node('generate_summary', generate_summary)  # 添加节点：生成总结
fa_builder.add_edge(START, 'get_failures')
fa_builder.add_edge('get_failures', 'generate_summary')  # 添加边：从获取失败的日志到生成总结
fa_builder.add_edge('generate_summary', END)  # 添加边，从生成总结到结束


# 定义问题总结状态的结构
class QuestionSummarizationState(TypedDict):
    docs: List[Logs]  # 日志列表
    qs_summary: str  # 问题总结
    report: str  # 报告

# 生成问题总结
def generate_summary(state):
    failures=state['failures']# 从状态中获取失败的日志
    # 添加函数:fa_summary=summarize(failures)
    fa_summary='Chroma文档检索质量差.'# 固定的总结内容
    return {'fa_summary': fa_summary}# 返回包含总结的字典
def send_to_slack(state):
    qs_summary=state['qs_summary']# 从状态中获取问题总结
    #添加函：  report=report_generation(qs_summary)
    report='foo bar baz' # 固定的报告内容
    return {'report':report}# 返回包含报告的字典

# 格式化报告以便在Slack 中发送

