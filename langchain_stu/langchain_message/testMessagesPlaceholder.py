# -*- coding: utf-8 -*-
# @Time : 2025/4/25 23:47
# @Author : nanji
# @Site :  https://zhuanlan.zhihu.com/p/656105088
# @File : testMessagesPlaceholder.py
# @Software: PyCharm 
# @Comment :
from langchain.prompts import MessagesPlaceholder
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

human_prompt = "Summarize our conversation so far in {word_count} words."
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages(
    [MessagesPlaceholder(variable_name="conversation"), human_message_template])

human_message = HumanMessage(content="What is the best way to learn programming?")
ai_message = AIMessage(content="""\
1. Choose a programming language: Decide on a programming language that you want to learn.

2. Start with the basics: Familiarize yourself with the basic programming concepts such as variables, data types and control structures.

3. Practice, practice, practice: The best way to learn programming is through hands-on experience\
""")

message = chat_prompt.format_prompt(conversation=[human_message, ai_message], word_count="10").to_messages()
print(message)
