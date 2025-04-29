# -*- coding: utf-8 -*-
# @Time : 2025/4/25 15:32
# @Author : nanji
# @Site :  https://www.bilibili.com/video/BV12iQBYWEx9/?p=5&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : chat_history_config.py
# @Software: PyCharm 
# @Comment :
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from dashscope import Generation
import os

# 加载环境变量
os.environ['OPENAI_API_KEY'] = ''
os.environ['OPENAI_BASE_URL'] = ''

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an assistant who's good at {ability}. Respond in 20 words or fewer"
        ),
        MessagesPlaceholder(variable_name='history'),
        ('human', '{input}'),
    ]
)

model = ChatOpenAI(model='gpt-4')
runnable = prompt | model
store = {}


def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history',
    history_factory_config=[
        ConfigurableFieldSpec(
            id='user_id',
            annotation=str,
            name='User ID',
            description='用户的唯一标识符',
            default='',
            is_shared=True
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name='Conversation ID',
            description='对话的唯一标识符',
            default='',
            is_shared=True
        )
    ]
)

response = with_message_history.invoke(
    {'ability': 'math', 'input': '余弦是什么意思?'},
    config={'configurable': {'user_id': '123', 'conversation_id': '1'}}
)
print(response)
# content='余弦是三角函数之一，用于表示直角三角形中邻边与斜边的比值，记为cos。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 32, 'prompt_tokens': 31, 'total_tokens': 63, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4-0613', 'system_fingerprint': 'fp_ee1d74bde0', 'id': 'chatcmpl-BRIVfjC7sykiUldhysduQk0AUaDYA', 'finish_reason': 'stop', 'logprobs': None} id='run-37f9f92e-b33b-463f-a99a-60f8d26782ed-0' usage_metadata={'input_tokens': 31, 'output_tokens': 32, 'total_tokens': 63, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

# 新的user_id --> 不记得了。
response = with_message_history.invoke(
    {'ability': 'math', 'input': '什么?'},
    config={'configurable': {'user_id': '123', 'conversation_id': '2'}}
)
print(response)
# content='我擅长数学。无论是简单的数学问题，还是复杂的计算，我都可以帮您解答。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 37, 'prompt_tokens': 32, 'total_tokens': 69, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4', 'system_fingerprint': None, 'id': 'chatcmpl-BRIVg8PkStExbsMyP2HygR5VPAuDw', 'finish_reason': 'stop', 'logprobs': None} id='run-8921b468-a6e8-40f7-a6f7-3fff53f68433-0' usage_metadata={'input_tokens': 32, 'output_tokens': 37, 'total_tokens': 69, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

