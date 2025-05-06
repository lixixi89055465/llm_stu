# -*- coding: utf-8 -*-
# @Time : 2025/5/6 20:34
# @Author : nanji
# @Site : 
# @File : tools_retriever.py
# @Software: PyCharm 
# @Comment :

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import Recursive
from langchain_text_splitters import CharacterTextSplitter,RecursiveCharacterTextSplitter
import os
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools.retriever import create_retriever_tool


os.environ['TAVILY_API_KEY'] = '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'
from langchain_community.tools.tavily_search import TavilySearchResults

loader=WebBaseLoader('https://baike.baidu.com/item/%E7%8C%AB/22261')
docs=loader.load()
documents=RecursiveCharacterTextSplitter(
    # chunk_size 参数在 RecursiveCharacterTextSplitter中用于指定每个文档快的最大字符数。他的作用主要有一下作用。
    # chunk_overlap 参数用于指定每个文档快之间的重叠字符数。这意味着，当文档被拆分成较小的快时，每个块的末尾部分都会与下一个快的开头部分重叠
    # 第一个快包含字符1到1000.第二个块包含字符 801,到1800.第三个快包含字符1601到2600
    chunk_size=1000,chunk_overlap=200
).split_documents(docs)

vector=FAISS.from_documents(documents, OpenAIEmbeddings())
retriever=vector.as_retriever()
print(retriever.invoke('猫的特征')[0])
retriever_tool=create_retriever_tool(
    retriever,
    'wiki_search',
    '搜索维基百科',
)


