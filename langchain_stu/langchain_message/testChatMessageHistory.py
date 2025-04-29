# -*- coding: utf-8 -*-
# @Time : 2025/4/26 8:45
# @Author : nanji
# @Site :  https://python.langchain.com.cn/docs/modules/memory/
# @File : testChatMessageHistory.py
# @Software: PyCharm 
# @Comment :
# from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()
history.add_user_message('hi!')
history.add_ai_message('whats up?')
print(history.messages)
print('1' * 100)
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message('hi!')
memory.chat_memory.add_ai_message('whats up?')
print(memory.load_memory_variables({}))

memory = ConversationBufferMemory(return_messages=True)
memory.chat_memory.add_user_message('hi!')
memory.load_memory_variables({"whats up? "})

print('2' * 100)
print(memory.load_memory_variables({}))
print('3' * 100)


from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(
    find_dotenv(),
    verbose=True  # 读取本地.env 文件，里面定义了OPENAI_API_KEY
)



from langchain.llms import OpenAI
from langchain.chains import ConversationChain


llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()
)

conversation.predict(input="Hi there!")