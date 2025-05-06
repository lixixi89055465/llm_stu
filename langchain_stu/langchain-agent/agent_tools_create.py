# -*- coding: utf-8 -*-
# @Time : 2025/5/6 20:34
# @Author : nanji
# @Site : https://blog.csdn.net/qq_45056135/article/details/141259495
# @File : tools_retriever.py
# @Software: PyCharm 
# @Comment :

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
import os
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools.retriever import create_retriever_tool

# os.environ['TAVILY_API_KEY'] = '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'
from langchain_community.tools.tavily_search import TavilySearchResults
import os

os.environ[
    'USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import \
    WebBaseLoader  # USER_AGENT environment variable not set, consider setting it to identify your requests.

loader = WebBaseLoader('https://baike.baidu.com/item/%E7%8C%AB/22261')
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    # chunk_size 参数在 RecursiveCharacterTextSplitter中用于指定每个文档快的最大字符数。他的作用主要有一下作用。
    # chunk_overlap 参数用于指定每个文档快之间的重叠字符数。这意味着，当文档被拆分成较小的快时，每个块的末尾部分都会与下一个快的开头部分重叠
    # 第一个快包含字符1到1000.第二个块包含字符 801,到1800.第三个快包含字符1601到2600
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)

vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()
print(retriever.invoke('猫的特征')[0])
retriever_tool = create_retriever_tool(
    retriever,
    'wiki_search',
    '搜索维基百科',
)

model = ChatOpenAI(model='gpt-4')
search = TavilySearchResults(max_results=1)
tools = [search, retriever_tool]
from langchain import hub

# 获取要使用的提示 - 您可以修改这个
prompt = hub.pull('hwchase17/openai-functions-agent')
print(prompt.messages)
from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(model, tools, prompt)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools)

