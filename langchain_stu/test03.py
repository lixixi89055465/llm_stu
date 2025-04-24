# -*- coding: utf-8 -*-
# @Time : 2025/4/24 16:14
# @Author : nanji
# @Site : 
# @File : test03.py
# @Software: PyCharm 
# @Comment :https://blog.csdn.net/shuz0612/article/details/145761831

'''
LLM的角色
“system“角色，通过分配特定行为给聊天助手来创建对话的上下文或范围。例如，如果您希望与ChatGPT在与体育相关的话题范围内进行对话，可以将”system"角色分配给聊天助手，并设置内容为"体育专家”。然后ChatGPT会表现得像体育专家一样回答您的问题。
"human"角色，代表实际的最终用户，他向ChatGPT发送提问。
"ai“角色，代表响应最终用户提示的实体。这个角色表示消息是助手（聊天模型）的响应。”ai"角色用于在当前请求中设置模型的先前响应，以保持对话的连贯性。
'''
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("DASH_SCOPE_API_KEY")
# 定义系统消息模板
system_template = "你是一个乐于助人的助手，总是用简洁的语言回答问题。"
system_message_prompt = SystemMessagePromptTemplate.from_template(
    system_template
)
# 定义用户消息模板
human_template = "请提供关于{topic}的简要信息。"
human_message_prompt = HumanMessagePromptTemplate.from_template(
    human_template
)
# 组合成聊天模板
chat_prompt = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        human_message_prompt
    ]
)

# 构成提升，填充占位符
prompt = chat_prompt.format_prompt(topic='LLM').to_messages()
print(prompt)

messages = chat_prompt.format_prompt(topic='LLM')
# 打印生成的消息
for message in messages:
    if isinstance(message, SystemMessage):
        print(f'System:{message.content}')
    elif isinstance(message, HumanMessage):
        print(f'Human :{message.content}')

print('1' * 100)

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

system_template = "你是一位助手，回复信息时语气偏向口语化。"
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "介绍关于{topic}的一个核心知识点。"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
# 创建 ChatPromptTemplate 实例
chat_prompt = ChatPromptTemplate.from_messages(
    [
        human_message_prompt,
        system_message_prompt
    ]
)

# 填充模板
messages = chat_prompt.format_messages(topic="LLM")
# 打印生成的消息
for message in messages:
    if isinstance(message, SystemMessage):
        print(f'System:{message.content}')
    elif isinstance(message, HumanMessage):
        print(f'Human:{message.content}')

# 嗲用模型
# model=ChatOllama(model='qwen2.5:3b')
# result=model(messages)
# # result=model.invoke(chat_prompt)
# print(result.content)


