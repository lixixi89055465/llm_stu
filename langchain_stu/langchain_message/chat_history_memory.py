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

# 加载环境变量
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'

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

response = with_message_history.invoke(
    {'ability': 'math', 'input': '什么?'},
    config={'configurable': {'session_id': "abc123"}}
)
print(response)

# 新的 session_id --> 不记得了 。
response = with_message_history.invoke(
    {'ability': 'math', 'input': '什么?'},
    config={'configurable': {'session_id': 'def234'}}
)
print(response)

# content='余弦是一个数学术语，在三角函数中，它表示在直角三角形中，邻边和斜边的比值。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 40, 'prompt_tokens': 38, 'total_tokens': 78, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4', 'system_fingerprint': None, 'id': 'chatcmpl-BRIKEpYQvmAZPvg5zwcwtVxUwr5In', 'finish_reason': 'stop', 'logprobs': None} id='run-9646c16c-9c48-4c0d-bfe0-85fd237304c3-0' usage_metadata={'input_tokens': 38, 'output_tokens': 40, 'total_tokens': 78, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# content='余弦是三角函数，定义为：直角三角形中邻边长度除以斜边长度的比值。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 31, 'prompt_tokens': 74, 'total_tokens': 105, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4-0613', 'system_fingerprint': 'fp_ee1d74bde0', 'id': 'chatcmpl-BRIKH6H2a9GPvMV47PWVFsUHeplmS', 'finish_reason': 'stop', 'logprobs': None} id='run-1e5cc9b2-58ca-41eb-85bc-71a46d61a4df-0' usage_metadata={'input_tokens': 74, 'output_tokens': 31, 'total_tokens': 105, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# content='对不起，我只能帮助计算或解析数学问题。请问你需要我帮助你解决什么问题呢？' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 40, 'prompt_tokens': 32, 'total_tokens': 72, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4', 'system_fingerprint': None, 'id': 'chatcmpl-BRIKI63vVx9WjtLcNg4Wmx8seb8Uu', 'finish_reason': 'stop', 'logprobs': None} id='run-d55cc5fc-56e2-4378-8301-51b6ebad99cb-0' usage_metadata={'input_tokens': 32, 'output_tokens': 40, 'total_tokens': 72, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

