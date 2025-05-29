# -*- coding: utf-8 -*-
# @Time : 2025/5/26 20:45
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1GdX6YGEnZ?t=1431.1
# @File : test08.py
# @Software: PyCharm 
# @Comment :

from openai import OpenAI


# 定义多伦对话方法
def run_chat_session():
    # 初始化模型
    model = OpenAI(base_url='http://localhost:8000/v1/', api_key='empty')
    # 初始化对话历史
    chat_history=[]
    # 启动对话循环
    while True:
        # 获取用户输入
        user_input=input('用户:')
        if user_input.lower()=='exit':
            print('退出对话.')
            break
        # 更新历史对话
        chat_history.append({'role':'user','content':user_input})
        # 调用模型对话
        try:
            chat_completion=model.chat.completions.create(
                messages=chat_history,
                # model='/home/nanji/workspace/Qwen2.5-0.5B-Instruct',
                model="qwen2_5_1_5",
            )
            # 获取最新回答
            model_response=chat_completion.choices[0]
            print('AI:',model_response.message.content)
            # 更新对话历史
            chat_history.append({'role':'assistant','content':model_response.message.content})
        except Exception as e:
            print('发生错误:',e)
            break

if __name__ == '__main__':
    run_chat_session()


