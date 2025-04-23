# -*- coding: utf-8 -*-
# @Time : 2025/4/22 21:28
# @Author : nanji
# @Site : 
# @File : chat_prompt.py
# @Software: PyCharm 
# @Comment :
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import SystemMessage

# 使用langchain定义的SystemMessage、HumanMessagePromptTemplate等工具类定义消息，
# 跟前面的例子类
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                '你是一个乐于助人的助手，可以润色内容，使其看起来更简单易读。'
            )
        ),
        HumanMessagePromptTemplate.from_template('{text}')
    ]
)
# 使用模型参数格式化模板
messages = chat_template.format_messages(text='我不喜欢吃好吃的东西')
print(messages)
