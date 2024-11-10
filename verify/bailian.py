# -*- coding: utf-8 -*-
# @Time    : 2024/11/10 下午5:06
# @Author  : nanji
# @Site    : 
# @File    : bailian.py
# @Software: PyCharm 
# @Comment : https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.791f7519fBamHk&accounttraceid=494cccbc11014cf1a6f54cba1bc77e68dsju#/model-market/detail/qwen-max-0428

import os
import random
from http import HTTPStatus
from dashscope import Generation
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# os.environ['DASHSCOPE_API_KEY'] = 'api_key'
api_key = os.environ['DASHSCOPE_API_KEY']


def call_stream_with_messages():
	messages = [
		{'role': 'user', 'content': '用萝卜，土豆，茄子做饭，给我个菜谱'}
	]
	response = Generation.call(

	)
	pass


client = OpenAI(
	# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
	# api_key=os.getenv("DASHSCOPE_API_KEY"),
	api_key=api_key,
	base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
	model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
	messages=[
		{'role': 'system', 'content': 'You are a helpful assistant.'},
		{'role': 'user', 'content': '你是谁？'}],
)

print(completion.model_dump_json())
