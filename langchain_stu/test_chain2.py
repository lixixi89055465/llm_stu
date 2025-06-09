# pip install Jinja2==3.0.0
from langchain_community.llms import Ollama
# from flask_api.RAG.config import base_url
from langchain_core.prompts import ChatPromptTemplate
import warnings
from flask_script import Manager
# 加载环境变量
import os

from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain

# os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
# os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
base_url = "http://localhost:11434"
warnings.filterwarnings('ignore', category=Warning)
content_en = '''
 My main responsibility is to provide natural language processing services to help users ask and answer questions through voice and text. I can answer questions on various topics, including but not limited to science and technology, life, culture and other topics. I can also have a conversation with you, so that you can get useful information more easily while enjoying intelligent services. Please feel free to tell me if you have any questions or need help!
'''

# llm = Ollama(base_url=base_url, model='qwen2:0.5b', temperature=0.6)
llm = Ollama(base_url=base_url, model='qwen2:latest', temperature=0.6)
prompt_template_1 = '请把以下内容翻译成中文，内容：{content}'

prompt = ChatPromptTemplate.from_template(prompt_template_1)
llm_chain_1 = LLMChain(llm=llm, prompt=prompt, verbose=True, output_key='chinese_content')
res = llm_chain_1.run({'content': content_en})

prompt_template_2 = '请对翻译后的内容进行总结或摘要，内容:{chinese_content}'
prompt = ChatPromptTemplate.from_template(prompt_template_2)
llm_chain_2 = LLMChain(llm=llm, prompt=prompt, verbose=True, output_key="chinese_summary")
res = llm_chain_2.run({'chinese_content': res})

prompt_template_3 = '以下内容是什么语言，内容:{chinese_summary}'
prompt = ChatPromptTemplate.from_template(prompt_template_3)
llm_chain_3 = LLMChain(llm=llm, prompt=prompt, verbose=True,
                       output_key='language')

prompt_template_4 = '请使用指定的语言对以下内容进行评论，内容：{chinese_summary},语言:{language}'
prompt = ChatPromptTemplate.from_template(prompt_template_4)
llm_chain_4 = LLMChain(llm=llm, prompt=prompt, verbose=True, output_key='review')

prompt_template_5 = '请对以下内容翻译成英文，并中英文双版本输出，内容{review}'
prompt = ChatPromptTemplate.from_template(prompt_template_5)
llm_chain_5 = LLMChain(llm=llm, prompt=prompt, verbose=True, output_key='two_language')

sequent_chain = SequentialChain(chains=[llm_chain_1, llm_chain_2, llm_chain_3, llm_chain_4, llm_chain_5],
                                input_variables=['content'],
                                output_variables=['chinese_content',
                                                  'chinese_summary',
                                                  'language',
                                                  'review',
                                                  'two_language'
                                                  ])
res = sequent_chain(content_en)
print(res)

'''
1号链：有输入，有输出
2号链：有输入，有输出。二号链的输入，是从 1 号链的输出这样获取来的 .
3号链：有输入，有输出。二号链的输入，是从 1 号链的输出这样获取来的 .
4号链：有输入，有输出。二号链的输入，是从 1 号链的输出这样获取来的 .
5号链：有输入，有输出。二号链的输入，是从 1 号链的输出这样获取来的 .
'''
