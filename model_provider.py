# -*- coding: utf-8 -*-
# @Time    : 2024/11/10 下午6:45
# @Author  : nanji
# @Site    : 
# @File    : model_provider.py
# @Software: PyCharm 
# @Comment :
import os
import json
import dashscope
from dashscope.api_entities.dashscope_response import Message
from prompt import user_prompt


class ModelProvider(object):
	def __init__(self):
		self.api_key = os.environ.get('API_KEY')
		self.model_name = os.environ.get('MODEL_NAME')
		self._client = dashscope.Generation()
		self.max_retry_time = 3

	def chat(self, prompt, chat_history):
		cur_retry_time = 0
		while cur_retry_time < self.max_retry_time:
			cur_retry_time += 1
			try:
				messages = [Message(role='system', content=prompt)]
				for his in chat_history:
					messages.append(Message(role='user', content=his[0]))
					messages.append(Message(role='assistant', content=his[1]))
				messages.append(Message(role='user', content=''))
				response = self._client.call(
					model=self.model_name,
					api_key=self.api_key,
					messages=messages
				)
				'''
				{
					"id": "chatcmpl-5112f6ac-0320-97a8-8dcb-7311aa46890e",
					"choices": [
						{
							"finish_reason": "stop",
							"index": 0,
							"logprobs": null,
							"message": {
								"content": "我是阿里云开发的一款超大规模语言模型，我叫通义千问。",
								"refusal": null,
								"role": "assistant",
								"audio": null,
								"function_call": null,
								"tool_calls": null
							}
						}
					],
					"created": 1731249273,
					"model": "qwen-plus",
					"object": "chat.completion",
					"service_tier": null,
					"system_fingerprint": null,
					"usage": {
						"completion_tokens": 17,
						"prompt_tokens": 22,
						"total_tokens": 39,
						"completion_tokens_details": null,
						"prompt_tokens_details": null
					}
				}
				'''
				content = json.load(response['choices'][0]['message'])




			except Exception as err:
				print('调用塔模型出错：{}'.format(err))
