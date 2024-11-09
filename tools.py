# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午3:16
# @Author  : nanji
# @Site    : 
# @File    : tools.py
# @Software: PyCharm
# @Comment :https://www.bilibili.com/video/BV1Sz421m7Rr?spm_id_from=333.788.player.switch&vd_source=50305204d8a1be81f31d861b12d4d5cf&p=4


import os
from langchain_community.tools.tavily_search import TavilySearchResults

'''
1.写文件 
2.读文件 
3.追加 
4.网络搜索 
'''


def _get_workdir_root():
	workdir_root = os.envision.get('WORKDIR_ROOT', './data/llm_result')
	return workdir_root


WORKDIR_ROOT = _get_workdir_root()


def read_file(filename):
	filename = os.path.join(WORKDIR_ROOT, filename)
	if not os.path.exists(filename):
		return f'{filename} not exist ,please check file exist before read'
	with open(filename, 'r') as f:
		return '\n'.join(f.readline())


def append_to_file(filename, content):
	filename = os.path.join(WORKDIR_ROOT, filename)
	if not os.path.exists(filename):
		return f'{filename} not exist ,please check  file exist before read'
	with open(filename, 'a') as f:
		f.write(content)
	return 'append content to file success'


def write_to_file(filename, content):
	filename = os.path.join(WORKDIR_ROOT, filename)
	if not os.path.exists(WORKDIR_ROOT):
		os.makedirs(WORKDIR_ROOT)
	with open(filename, 'w') as f:
		f.write(content)
	return 'write content to file success'


def search(query):
	tavily = TavilySearchResults(max_results=5)
	try:
		ret = tavily.invoke(input=query)
		'''
		ret:
		[{
			'content':'',
			'url':''
		}]
		'''
		content_list = [obj['content'] for obj in ret]
		return '\n'.join(content_list)
	except Exception as err:
		return 'search err:{}'.format(err)


tools_info = [
	{
		"name": 'read_file',
		'description': 'readf file from agent generate,should write file before read',
		'args': [
			{
				'name': 'filename',
				'type': 'string',
				'description': 'read file name'
			}
		]
	},
	{
		'name': 'write_to_file',
		'description': 'write llm content to file',
		'args': [{
			'name': 'filename',
			'type': 'string',
			'description': 'file name'
		}, {
			'name': 'content',
			'type': 'string',
			'description': 'write to file content'
		}]
	},
	{
		'name': 'search',
		'description': 'this is a search engine,'
					   'you can gain additional knowledge though this search engine '
					   'when you are unsure of what large model return ',
		'args': [{
			'name': 'query',
			'type': 'string',
			'description': 'search query to look up'
		}]
	},
]
tools_map = {
	'read_file': read_file,
	'append_to_file': append_to_file,
	'write_to_file': write_to_file,
	'search': search
}

