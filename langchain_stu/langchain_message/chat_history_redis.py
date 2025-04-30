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
import os
# os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
# os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            "You're an assistant who's good at {ability}.Respond in 20 words or fewer",
        ),
        MessagesPlaceholder(variable_name='history'),
        ('human', '{input}')
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

# content='余弦是一个三角函数，常标记为 cos。它是直角三角形的邻边长度与斜边长度的比值。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 39, 'prompt_tokens': 38, 'total_tokens': 77, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4-0613', 'system_fingerprint': None, 'id': 'chatcmpl-BRgN26Y3ZQ4s3iSnHyqLeZMCVl7Y2', 'finish_reason': 'stop', 'logprobs': None} id='run-456a9bd6-6c6f-43be-8f38-00d6317a44cc-0' usage_metadata={'input_tokens': 38, 'output_tokens': 39, 'total_tokens': 77, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# content='余弦是一个数学概念，它衡量了直角三角形的一个角的邻边与斜边之间的比例。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 42, 'prompt_tokens': 89, 'total_tokens': 131, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4', 'system_fingerprint': None, 'id': 'chatcmpl-BRgN6uuQ2XIbFnWxaH3KFnGcFK6bK', 'finish_reason': 'stop', 'logprobs': None} id='run-809d9e9a-40c4-4473-b45d-b8dae72e2d22-0' usage_metadata={'input_tokens': 89, 'output_tokens': 42, 'total_tokens': 131, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# content='对不起，我可能没有明白您的问题。您能具体说明您需要数学帮助的地方吗?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 33, 'prompt_tokens': 32, 'total_tokens': 65, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4-0613', 'system_fingerprint': None, 'id': 'chatcmpl-BRgN9s9hrB2i5BxAWJAMHDjk4eWG9', 'finish_reason': 'stop', 'logprobs': None} id='run-cd7ba1ee-ef9e-4081-96d3-785112434691-0' usage_metadata={'input_tokens': 32, 'output_tokens': 33, 'total_tokens': 65, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

