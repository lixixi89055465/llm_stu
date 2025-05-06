# -*- coding: utf-8 -*-
# @Time : 2025/5/6 20:34
# @Author : nanji
# @Site : 
# @File : tools_retriever.py
# @Software: PyCharm 
# @Comment :

import os

os.environ['TAVILY_API_KEY'] = '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'
from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=2)
print(search.invoke('今天上海天气怎么样?'))
