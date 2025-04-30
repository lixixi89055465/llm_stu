# -*- coding: utf-8 -*-
# @Time : 2025/4/30 17:49
# @Author : nanji
# @Site : 
# @File : test02.py
# @Software: PyCharm 
# @Comment :
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool


from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(query: str) -> str:
    """Look up things online."""
    return "LangChain"

print(search.name)
print(search.description)
print(search.args)

res = search.run({"query": "start test"})
print(res)
