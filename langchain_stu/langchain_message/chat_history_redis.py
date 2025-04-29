# -*- coding: utf-8 -*-
# @Time : 2025/4/28 21:13
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9?spm_id_from=333.788.player.switch&vd_source=50305204d8a1be81f31d861b12d4d5cf&p=5
# @File : chat_history_redis.py
# @Software: PyCharm 
# @Comment :

# 引入 redis 聊天消息存储类
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            "You're an assistant who's good at {ability}.Respond in 20 words or fewer",
        ),
        MessagesPlaceholder(variable_name='history'),
        ('human', '{input')
    ]
)
model = ChatOpenAI(model='gpt-4')
runnable = prompt | model
store = {}
REDIS_URL = 'redis://localhost:6379/0'


def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=REDIS_URL)


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key='input',
    history_messages_key='history'
)

response = with_message_history.invoke(
    {'ability': 'math', 'input': '余弦是什么意思?'},
    config={'configurable': {"session_id": "abc123"}}
)

print(response)

response = with_message_history.invoke(
    {'ability': 'math', 'input': '什么?'},
    config={'configurable': {"session_id": "abc123"}}
)
print(response)

# 新的session_id --> 不记得了。
response = with_message_history.invoke(
    {'ability': 'math', 'input': '什么?'},
    config={'configurable': {"session_id": "def234"}}
)

print(response)
