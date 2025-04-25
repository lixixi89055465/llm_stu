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

prompt = ChatPromptTemplate.from_template(
    [
        (
            "system",
            "You're an assistant who's good at {ability}. Respond in 20 words or fewer"
        ),
        MessagesPlaceholder(variable_name='history'),
        ('human', '{input}'),
    ]
)

model=ChatOpenAI(model='gpt-4')
runnable=prompt| model
store={}
