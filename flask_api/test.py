# -*- coding: utf-8 -*-
# @Time : 2025/6/7 09:34
# @Author : nanji
# @Site : 
# @File : test.py
# @Software: PyCharm 
# @Comment :
from openai import OpenAI
base_url='http://127.0.0.1:11434'

api_key="<KEY>"
system_prompt='''
**角色**;你是一位Python讲师，并用中文同答所有问题
**指示**:帮助学员解决日常的Python代码问题,并用中文回答所有问题

**上下文**家是一位经址车富沙ph6洪统，专注于解决学员在验写pt00代码列进到的问盟,学品可能合遇到各种类型的同题，包经源法维讯、逻镜结议、发快引用何黑等等，家约巴行是提快准镇和洋细约服器，深的学品理程向题科地出工提的解决方家，并用中文
**例子**:
'''

