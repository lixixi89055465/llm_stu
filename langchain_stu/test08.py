# -*- coding: utf-8 -*-
# @Time : 2025/4/24 21:33
# @Author : nanji
# @Site : 
# @File : test08.py
# @Software: PyCharm 
# @Comment :

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(
    find_dotenv(),
    verbose=True  # 读取本地.env 文件，里面定义了OPENAI_API_KEY
)
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4.1",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
