# -*- coding: utf-8 -*-
# @Time : 2025/6/13 23:11
# @Author : nanji
# @Site : 
# @File : test_graph_test.py
# @Software: PyCharm 
# @Comment :

from fastapi import FastAPI, File, UploadFile

from pydantic import BaseModel, Field
from starlette.websockets import WebSocket

# from flask_api.project.graph_test import langGraph
# from graph_test import langGraphLearn
from rag_tool_graph import ChatDoc
# 加载环境变量
import os

os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
# os.environ['OPENAI_API_KEY'] = ''
# os.environ['OPENAI_BASE_URL'] = ''
chat = ChatDoc()
app = FastAPI()


class RagInput(BaseModel):
    question: str = Field(description='问题')


@app.post('/upload_file')
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename
    with open(filename, 'wb') as f:
        f.write(contents)
    chat.get_file(filename)
    chat.split_sentence(filename)
    chat.vector_storage()
    return 'success'


@app.post('/question')
async def search(question: RagInput):
    result = chat.chat_with_doc(question.question)
    return {'result': result}


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = app.run_langgraph(question=data)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
