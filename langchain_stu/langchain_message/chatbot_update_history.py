# -*- coding: utf-8 -*-
# @Time : 2025/4/29 22:39
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV12iQBYWEx9/?p=5&spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=50305204d8a1be81f31d861b12d4d5cf
# @File : chatbot_update_history.py
# @Software: PyCharm 
# @Comment :
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
import os

os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'

temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message('我叫Jack,你好 ')
temp_chat_history.add_ai_message('你好')
temp_chat_history.add_user_message('你今天心情挺开心')
temp_chat_history.add_ai_message('你今天心情怎么样')
temp_chat_history.add_user_message('我下午在打篮球')
temp_chat_history.add_ai_message('你下午在做什么 ')

print(temp_chat_history.messages)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '你是一个乐于助人的助手。尽力回答所有问题。提供的聊天历史包括与您交谈的用户的事实。'
        ),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{input}'),
    ]
)
chat = ChatOpenAI(model='gpt-4')
chain = prompt | chat


def trim_messages(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) <= 2:
        return False
    temp_chat_history.clear()
    for message in stored_messages[-2:]:
        temp_chat_history.add_message(message)
    return True


chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: temp_chat_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)
chain_with_trimming = (
        RunnablePassthrough.assign(message_trimmed=trim_messages)
        | chain_with_message_history
)

response = chain_with_trimming.invoke(
    {'input': '我叫什么 ?'},
    {'configurable': {'session_id': 'unused'}}
)
print(response.content)
print(temp_chat_history.messages)
# [HumanMessage(content='我叫Jack,你好 ', additional_kwargs={}, response_metadata={}), AIMessage(content='你好', additional_kwargs={}, response_metadata={}), HumanMessage(content='你今天心情挺开心', additional_kwargs={}, response_metadata={}), AIMessage(content='你今天心情怎么样', additional_kwargs={}, response_metadata={}), HumanMessage(content='我下午在打篮球', additional_kwargs={}, response_metadata={}), AIMessage(content='你下午在做什么 ', additional_kwargs={}, response_metadata={})]
# 哦，那你的篮球比赛怎么样？你玩得开心吗？
# [HumanMessage(content='我下午在打篮球', additional_kwargs={}, response_metadata={}), AIMessage(content='你下午在做什么 ', additional_kwargs={}, response_metadata={}), HumanMessage(content='我下午在打篮球', additional_kwargs={}, response_metadata={}), AIMessage(content='哦，那你的篮球比赛怎么样？你玩得开心吗？', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 27, 'prompt_tokens': 91, 'total_tokens': 118, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4-0613', 'system_fingerprint': None, 'id': 'chatcmpl-BRsT9ORLyWmBPAbPY3wZ6r8qW5K5f', 'finish_reason': 'stop', 'logprobs': None}, id='run-d693e2e5-ae06-45ce-8241-3f56a8e5e853-0', usage_metadata={'input_tokens': 91, 'output_tokens': 27, 'total_tokens': 118, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]
# {'input': '我叫什么 ?'},
# [HumanMessage(content='我叫Jack,你好 ', additional_kwargs={}, response_metadata={}), AIMessage(content='你好', additional_kwargs={}, response_metadata={}), HumanMessage(content='你今天心情挺开心', additional_kwargs={}, response_metadata={}), AIMessage(content='你今天心情怎么样', additional_kwargs={}, response_metadata={}), HumanMessage(content='我下午在打篮球', additional_kwargs={}, response_metadata={}), AIMessage(content='你下午在做什么 ', additional_kwargs={}, response_metadata={})]
# 抱歉，我没有你的名字信息。你能告诉我吗？
# [HumanMessage(content='我下午在打篮球', additional_kwargs={}, response_metadata={}), AIMessage(content='你下午在做什么 ', additional_kwargs={}, response_metadata={}), HumanMessage(content='我叫什么 ?', additional_kwargs={}, response_metadata={}), AIMessage(content='抱歉，我没有你的名字信息。你能告诉我吗？', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 22, 'prompt_tokens': 90, 'total_tokens': 112, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4-0613', 'system_fingerprint': None, 'id': 'chatcmpl-BRsbQHHvHJUsegFYkum9jLNg3HNbS', 'finish_reason': 'stop', 'logprobs': None}, id='run-c4f4045d-4e11-4989-b004-8d63a3279a8e-0', usage_metadata={'input_tokens': 90, 'output_tokens': 22, 'total_tokens': 112, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]

