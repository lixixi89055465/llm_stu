# -*- coding: utf-8 -*-
# @Time : 2025/4/30 12:01
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?p=5&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : chatbot_summarize_history.py
# @Software: PyCharm 
# @Comment :
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
import os
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
chat = ChatOpenAI(model='gpt-4')
temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message('我叫Jack,你好')
temp_chat_history.add_ai_message('你好')
temp_chat_history.add_user_message('我今天心情挺开心 ')
temp_chat_history.add_ai_message('你今天心情怎么样')
temp_chat_history.add_user_message('我下午在打篮球')
temp_chat_history.add_ai_message('你下午在做什么')
print(temp_chat_history.messages)

prompt = ChatPromptTemplate.from_messages(
    [
        ('system',
         '你是一个乐于助人的助手。尽力回答所有问题。提供的聊天历史包括与您交谈的用户的事实。'
         ),
        MessagesPlaceholder(variable_name='chat_history'),
        ('user', '{input}'),
    ],
)
chain = prompt | chat
chat_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: temp_chat_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)


def summarize_messages(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) == 0:
        return False
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name='chat_history'),
            (
                'user',
                '将上述聊天消息浓缩成一条摘要消息。尽可能包含多个具体细节。'),
        ]
    )
    summarization_chain = summarization_prompt | chat
    summary_message = summarization_chain.invoke({'chat_history': stored_messages})
    temp_chat_history.clear()
    temp_chat_history.add_message(summary_message)
    return True


chain_with_summarization = (
        RunnablePassthrough.assign(messages_summarized=summarize_messages)
        | chat_with_message_history
)
response = chain_with_summarization.invoke(
    {'input': '名字，下午在干嘛，心情'},
    {'configurable': {'session_id': 'unused'}}
)
print(response.content)
print(temp_chat_history.messages)

# 用户的名字是 Jack，下午他去打篮球了，他今天的心情非常开心。
# [AIMessage(content='"Jack今天心情开心，并且他在下午时分打篮球。"', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 23, 'prompt_tokens': 108, 'total_tokens': 131, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4', 'system_fingerprint': None, 'id': 'chatcmpl-BRwapxOYNv1iYwDZN9wVIKXW4DpLW', 'finish_reason': 'stop', 'logprobs': None}, id='run-55a8f2aa-b77c-4475-8847-75ffe7993e1b-0', usage_metadata={'input_tokens': 108, 'output_tokens': 23, 'total_tokens': 131, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}), HumanMessage(content='名字，下午在干嘛，心情', additional_kwargs={}, response_metadata={}), AIMessage(content='用户的名字是 Jack，下午他去打篮球了，他今天的心情非常开心。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 28, 'prompt_tokens': 98, 'total_tokens': 126, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4-0613', 'system_fingerprint': None, 'id': 'chatcmpl-BRwasa7Hb1X5JXiuPonEsZb1bvn2r', 'finish_reason': 'stop', 'logprobs': None}, id='run-93c7a252-035a-4bb3-905c-444e312cea8d-0', usage_metadata={'input_tokens': 98, 'output_tokens': 28, 'total_tokens': 126, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]

