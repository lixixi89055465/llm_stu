# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 上午8:30
# @Author  : nanji
# @Site    : 
# @File    : cli_main.py
# @Software: PyCharm 
# @Comment :https://www.bilibili.com/video/BV1Sz421m7Rr?spm_id_from=333.788.videopod.episodes&vd_source=50305204d8a1be81f31d861b12d4d5cf
import time


def parse_thoughts(response):
	'''
response:
		{
			'action':{
				'name':'action name',
				'args':{
					'args name':'args value'
				}
			},
			'thoughts':
			{
				'text':'thought',
				'plan':'plan',
				'criticism':'criticism',
				'speak':'speak',
				'reasoning':'',
			}
		}
	:param response:
	:return:
	'''
	try:
		thoughts = response.get('thoughts')
		observation = thoughts.get('speak')
		plan = thoughts.get('plan')
		reasoning = thoughts.get('reasoning')
		criticism = thoughts.get('criticism')
		prompt = f'plan:{plan} \n reasoning: {reasoning}\n' \
			f'criticism:{criticism}\nobservation:{observation}'
		return prompt

	except Exception as err:
		print('parse thoughts err: {}'.format(err))
		return ''.format(err)


def agent_execute(query, max_request_time):
	cur_request_time = 0
	chat_history = []
	agent_scratch = ''
	while cur_request_time < max_request_time:
		cur_request_time += 1
		'''
		如果返回结果达到预期，则直接返回 
		'''
		'''
		prompt包含的功能：
			1。任务描述 
			2。工具描述 
			3。用户的输入user_msg
			4.assistant_msg
			5.限制 
			6.给出更好实践的描述 
			
			
		'''
		prompt = gen_prompt(query, agent_scratch)
		start_time = time.time()
		print('********** {}. 开始调用塔模型llm'.format(cur_request_time), flush=True)
		# call llm
		response = call_llm()
		end_time = time.time()
		print('***********{}。调用塔模型结束，耗时：{}.......'.format(cur_request_time, end_time - start_time))
		if not response or not isinstance(response, dict):
			print('调用大模型错误，即将重试.....', response)
			continue
		'''
		response:
		{
			'action':{
				'name':'action name',
				'args':{
					'args name':'args value'
				}
			},
			'thoughts':
			{
				'text':'thought',
				'plan':'plan',
				'criticism':'criticism',
				'speak':'speak',
				'reasoning':'',
			}
		}
		'''
		action_info = response.get('action')
		action_name = action_info.get('name')
		action_args = action_info.get('args')
		print('当前action name:', action_name, action_args)
		if action_name == 'finish':
			final_answer = action_args.get('answer')
			print('final_answer:', final_answer)
			break
		observation = response.get('thoughts').get('speak')

		try:
			'''
			action_name 到 函数的映射 map-> {action_name: } 
			'''
			# todo: tools_map 的实现
			tools_map = {}
			func = tools_map.get(action_name)
			observation = func(**action_args)
		except Exception as err:
			print('调用工具一场:', err)
		agent_scratch = agent_scratch + '\n' + observation

		user_msg = '决定使用哪一个工具'
		assistant_msg = parse_thoughts(response)
		chat_history.append([user_msg, assistant_msg])


def main():
	max_request_time = 10
	while True:
		query = input("请输入您的目标 ")
		if query == 'exit':
			return
		agent_execute(query, max_request_time=max_request_time)


if __name__ == '__main__':
	main()
