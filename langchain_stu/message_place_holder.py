# -*- coding: utf-8 -*-
# @Time : 2025/4/22 22:06
# @Author : nanji
# @Site : 
# @File : message_place_holder.py
# @Software: PyCharm 
# @Comment :
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

prompt_template = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful assistant'),
    MessagesPlaceholder('msgs')
])
result = prompt_template.invoke({'msgs':
                                     [HumanMessage(content='hi!'),
                                      HumanMessage(content='hello!')]
                                 })

print(result)
