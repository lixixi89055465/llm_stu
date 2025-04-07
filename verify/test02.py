# -*- coding: utf-8 -*-
# @Time    : 2024/11/10 下午6:41
# @Author  : nanji
# @Site    : 
# @File    : create_collection.py
# @Software: PyCharm 
# @Comment :https://bailian.console.aliyun.com/?switchAgent=10375023&productCode=p_efm#/model-market/detail/qwen1.5-110b-chat


import os
import random
from http import HTTPStatus
from dashscope import Generation
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
	# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
	api_key=os.getenv("DASHSCOPE_API_KEY"),
	base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
	model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
	messages=[
		{'role': 'system', 'content': 'You are a helpful assistant.'},
		{'role': 'user', 'content': '你是谁？'}],
)

print(completion.model_dump_json())