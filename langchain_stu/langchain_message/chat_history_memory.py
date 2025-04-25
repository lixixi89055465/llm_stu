# -*- coding: utf-8 -*-
# @Time : 2025/4/25 11:09
# @Author : nanji
# @Site : 
# @File : chat_history_memory.py
# @Software: PyCharm 
# @Comment :
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("DASH_SCOPE_API_KEY")



# 创建一个聊天提示词模板
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an assistant who's good at {ability}. Respond in 20 words or fewer",
        ),
        # 历史消息占位符
        MessagesPlaceholder(variable_name='history'),
        ('human', '{input}')
    ]
)
model = ChatOpenAI(model='gpt-4')

runnable = prompt | model
store = {}


# 定义一个获取会画历史的函数，入参是 session_id,返回一个会话历史记录
def get_session_hitory(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# 创建一个带会话历史记录
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_hitory,
    input_messages_key='input',
    history_messages_key='history'
)
# 调用带会话历史记录的 Runnable
response = with_message_history.invoke(
    {'ability': 'math', 'input': '余弦是什么意思？'},
    config={'configurable': {"session_id": "abc123"}}
)
print(response)
# 新的 session_id --> 不记得了 。
response = with_message_history.invoke(
    {'ability': 'math', 'input': '什么?'},
    config={'configurable': {'session_id': 'def234'}}
)
print(response)
