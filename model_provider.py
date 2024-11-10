# -*- coding: utf-8 -*-
# @Time    : 2024/11/10 下午6:45
# @Author  : nanji
# @Site    : 
# @File    : model_provider.py
# @Software: PyCharm 
# @Comment :
import os
import dashscope


class ModelProvider(object):
	def __init__(self):
		self.api_key = os.environ.get('API_KEY')
		self.model_name = os.environ.get('MODEL_NAME')
		self._client = dashscope.Generation()
		self.max_retry_time = 3

	def chat(self, prompt, chat_history):
		pass
