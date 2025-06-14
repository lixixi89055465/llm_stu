# -*- coding: utf-8 -*-
# @Time : 2025/6/12 20:38
# @Author : nanji
# @Site : 
# @File : test_langchain_function_call.py
# @Software: PyCharm 
# @Comment :
'''

基于 langchain 去使用 function_call
function_call 调用高德 api获取经纬度，并通过经纬度拿到附近的商店
'''
import os
import json
from langchain_experimental.llms.ollama_functions import OllamaFunctions

from langchain.schema import (
    HumanMessage,
    FunctionMessage
)
from langchain_openai import ChatOpenAI
import requests

os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
# os.environ['OPENAI_API_KEY'] = 'aa'
# os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
# api_key = os.environ['OPENAI_API_KEY']
# os.environ['SERPAPI_API_KEY']=''
os.environ["SERPAPI_API_KEY"] = "d4dd7f852c4a8468fe1468814b56ad7f11af487c013b1cee8c1f74c2289c0835"
# model = ChatOpenAI(temperature=0, model='qwen2:latest')
base_url = "http://192.168.11.178:11434/v1"

llm = ChatOpenAI(model='qwen2:latest', temperature=0,
                 base_url=base_url, api_key='empty')


def search_around(keyword, location):
    around_url = "https://restapi.amap.com/v5/place/around"
    params = {
        "key": "92704d87499df4ffbe85fbf28d1b6815",
        "keywords": keyword,
        "location": location
    }
    res = requests.get(url=around_url, params=params)
    prompt = "请帮我整理以下内容中的名称，地址和距离，并按照地址与名称对应输出，且告诉距离多少米，内容:{}".format(
        res.json())
    result = llm.invoke(prompt)
    return result + "\nend"


def get_location(keyword):
    url = "https://restapi.amap.com/v5/place/text"
    params = {
        "key": "92704d87499df4ffbe85fbf28d1b6815",
        "keywords": keyword,
    }
    res = requests.get(url=url, params=params)
    return '{}的经纬度是：'.format(keyword) + res.json()["pois"][0]["location"]


base_url = "http://192.168.11.178:11434/v1"
# function_ollama = OllamaFunctions(
#     base_url=base_url,
#     api_key='empty',
#     model='qwen2:72b'
# )
function_ollama = OllamaFunctions(base_url=base_url,
                                  api_key="empty",
                                  model="qwen2:latest")

functions = [{
    "name": "get_location",
    "description": "根据用户输入的地理位置，使用高德的API接口查询出对应的经纬度",
    "parameters": {
        "keyword": {
            "type": "string",
            "description": "用户输入的地理位置",
        },
        "required": ["keyword"]
    }
},
    {"name": "search_around",
     "description": "根据提供的经纬度和行业类型，使用高德API接口搜索出附近对应的行业店铺",
     "parameters": {
         "keyword": {
             "type": "string",
             "description": "行业的关键字",
         },
         "location": {
             "type": "string",
             "description": "根据get_location方法提供的经纬度",
         }
     },
     "required": ["keyword", "location"]
     }]

# messages = [HumanMessage(content='请告诉我四川大学望江校区的经纬度是多少?')]
messages = [HumanMessage(content='请告诉我四川大学望江校区附近最近的超市')]
message = llm.predict_messages(messages=messages, functions=functions)
status = message.response_metadata.get('finish_reason')

function_map = {
    "search_around": search_around,
    "get_location": get_location
}
print(message.content)
while status == 'function_call':
    function_name = message.additional_kwargs['function_call']['name']
    arguments = json.load(message.additional_kwargs['function_call']['arguments'])
    function_response = function_map[function_name](**arguments)
    messages.append(FunctionMessage(
        name=message.additional_kwargs['function_call']['name'],
        content=function_response
    ))
    message = llm.predict_messages(messages=messages, functions=functions)
    status = message.response_metadata.get('finish_reason')
