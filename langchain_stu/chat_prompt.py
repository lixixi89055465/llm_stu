# -*- coding: utf-8 -*-
# @Time : 2025/4/22 21:28
# @Author : nanji
# @Site : 
# @File : chat_prompt.py
# @Software: PyCharm 
# @Comment :
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
# api_key = os.environ.get("DASH_SCOPE_API_KEY")

# 通过一个消息数组创建聊天消息模板
# 数组每一个元素代表一条消息，每个消息元组，第一个元素代表消息角色（也成为消息类型）
# 第二个元素代表消息内容。
# 消息角色：system 代表系统消息，human 代表人类消息，ai代表LLM返回的消息内容
# 下面消息定义了2个模板参数name 和user_input

chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', '你是一位人工只能助手,你的名字是{name}'),
        ('human', '你好'),
        ('ai', '我很好，谢谢!'),
        ('human', '{user_input}')
    ]
)
# 通过模板参数格式化模板内容
messages = chat_template.format_messages(name='Bob', user_input='你的名字叫什么?')
print(messages)
