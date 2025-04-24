# -*- coding: utf-8 -*-
# @Time : 2025/4/24 21:18
# @Author : nanji
# @Site : https://zhuanlan.zhihu.com/p/689629713
# @File : test06.py
# @Software: PyCharm 
# @Comment :
# 这是一个Python代码片段，用于创建一个FastAPI应用
# 并添加一个使用Anthropic模型的路由
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatAnthropic
from langserve import add_routes

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# 添加路由到应用中
add_routes(
    app,
    ChatAnthropic(),
    path="/anthropic",
)

# 创建一个讲笑话的模板
model = ChatAnthropic()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

# 如果你直接运行这个Python脚本，它会启动一个服务器
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
