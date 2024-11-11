# -*- coding: utf-8 -*-
# @Time    : 2024/11/11 下午10:57
# @Author  : nanji
# @Site    : 
# @File    : aa.py
# @Software: PyCharm 
# @Comment :
a = '''
{
	'action':{
		'name':'write_to_file',
		'args':{
			'filename':'hello.txt',
			'content':'你好'
		}
	},
	'thoughts':
	{
		'plan':'首先，将问候语“你好”写入文件，以此来响应用户的需求，虽然这里没有直接与用户交流的命令，但通过创建一个包含问候的文件，间接实现了友好的互动。',
		'criticism':'在当前限制条件下，无法直接向用户传达问候，只能通过间接方式，这可能不是最直观的交流方式，但遵循了规则限制。',
		'speak':'已经为您准备了一个包含“你好”的文件。',
		'reasoning':'由于限制条件不允许直接交互或提及法律问题，采取了写入文件这一动作，既遵守规则又能体现回应意图。'
	}
}
'''
import json

a=a.replace('\'','\"')
print(a)
res = json.loads(a)
print('0' * 100)
print(res)
