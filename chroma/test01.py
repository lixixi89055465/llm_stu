# !pip install --upgrade openai
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from openai import OpenAI
import os
# 加载 环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(
    find_dotenv(),
    verbose=True  # 读取本地.env 文件，里面定义了OPENAI_API_KEY
)

client = OpenAI()


def get_embeddings(texts, model='text-embedding-ada-002', dimensions=None):
    '''封装OpenAI 的Embedding 模型接口 '''
    if model == 'text-embedding-ada-002':
        dimensions = None
    if dimensions:
        data = client.embeddings.create(
            input=texts, model=model,
            dimensions=dimensions
        ).data


def extract_text_from_pdf(filename,  #
                          page_numbers=None,  #
                          min_line_length=1):
    '''
    从pdf文件中（按指定页码）提取文字
    '''
    paragraphs = []
    buffer = ''
    full_text = ''
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳出范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'
    # 按照空行分割，将文本重新组织成段落
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' ' + text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


paragraphs = extract_text_from_pdf("llama2.pdf", min_line_length=10)

# for para in paragraphs[:4]:
#     print(para + "\n")

from openai import OpenAI
import os

# 加载环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv(), verbose=True)  # 读取本地 .env 文件，里面定义了 OPENAI_API_KEY



def get_completion(prompt, model="gpt-4o"):
    '''封装 openai 接口'''
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content


def build_prompt(prompt_template, **kwargs):
    '''将 Prompt 模板赋值'''
    inputs = {}
    for k, v in kwargs.items():
        if isinstance(v, list) and all(isinstance(elem, str) for elem in v):
            val = '\n\n'.join(v)
        else:
            val = v
        inputs[k] = val
    return prompt_template.format(**inputs)


prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。

已知信息:
{context} # 检索出来的原始文档

用户问：
{query} # 用户的提问

如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。
请不要输出已知信息中不包含的信息或答案。
请用中文回答用户问题。
"""
import chromadb
from chromadb.config import Settings


class MyVectorDBConnector:
    def __init__(self, collection_name, embedding_fn):
        # 内存模式
        chroma_client = chromadb.Client(Settings(allow_reset=True))
        # 数据持久化
        # chroma_client=chromadb.PersistentClient(path='./chroma')
        # 注意：为了演示，实际不需要每次reset(),并且是不可逆的！
        chroma_client.reset()
        # 创建一个collection
        self.collection = chroma_client.get_or_create_collection(
            name=collection_name
        )
        self.embedding_fn = embedding_fn

    def add_document(self, documents):
        '''向 collection中添加文档与变量 '''
        self.collection.add(
            embeddings=self.embedding_fn(documents),  # 每个文档的向量
            documents=documents,  # 文档的原文
            ids=[f'id{i}' for i in range(len(documents))]  # 每个文档的id
        )

    def search(self, query, top_n):
        '''检索向量数据库 '''
        results = self.collection.query(
            query_embeddings=self.embedding_fn([query]),
            n_results=top_n
        )
        return results


import numpy as np
from numpy import dot
from numpy.linalg import norm


def cos_sim(a, b):
    '''余弦距离 -- 越大越相似'''
    return dot(a, b) / (norm(a) * norm(b))


def l2(a, b):
    '''欧氏距离 -- 越小越相似'''
    x = np.asarray(a) - np.asarray(b)
    return norm(x)


def get_embeddings(texts, model="text-embedding-ada-002", dimensions=None):
    '''封装 OpenAI 的 Embedding 模型接口'''
    if model == "text-embedding-ada-002":
        dimensions = None
    if dimensions:
        data = client.embeddings.create(
            input=texts, model=model, dimensions=dimensions).data
    else:
        data = client.embeddings.create(input=texts, model=model).data
    return [x.embedding for x in data]


test_query = ["测试文本"]
# vec = get_embeddings(test_query)[0]
# print(f"Total dimension: {len(vec)}")
# print(f"First 10 elements: {vec[:10]}")

# 创建一个向量数据库对象
vector_db = MyVectorDBConnector(
    'demo',
    get_embeddings
)
# 向向量数据库中添加文档
vector_db.add_document(paragraphs)
user_query = 'Llama 2有多少参数'
# user_query = 'Does Llama 2 have a conversational variant'
# results = vector_db.search(user_query, 2)


# for para in results['documents'][0]:
#     print(para + '\n')


class RAG_Bot:
    def __init__(self, vector_db, llm_api, n_results=2):
        self.vector_db = vector_db
        self.llm_api = llm_api
        self.n_results = n_results

    def chat(self, user_query):
        # 1.检索
        search_results = self.vector_db.search(user_query, self.n_results)
        # 2.构建 Prompt
        prompt = build_prompt(
            prompt_template,
            context=search_results['documents'][0], query=user_query
        )
        # 3.调用 LLM
        response = self.llm_api(prompt)
        return response


# 创建一个 RAG 机器人
bot = RAG_Bot(
    vector_db,
    llm_api=get_completion
)
user_query = 'llama 2有多少参数?'
response = bot.chat(user_query)
# print(response)

# model = 'text-embedding-3-large'
model='text-embedding-ada-002'
dimensions = 128
query='国际争端'
# 且能支持多国语言
# query = 'global conflicts'
documents = [
    "联合国就苏丹达尔富尔地区大规模暴力事件发出警告",
    "土耳其、芬兰、瑞典与北约代表将继续就瑞典“入约”问题进行谈判",
    "日本岐阜市陆上自卫队射击场内发生枪击事件 3人受伤",
    "国家游泳中心（水立方）：恢复游泳、嬉水乐园等水上项目运营",
    "我国首次在空间站开展舱外辐射生物学暴露实验",
]
query_vec = get_embeddings([query], model=model, dimensions=dimensions)[0]
doc_vecs = get_embeddings(documents, model=model, dimensions=dimensions)
print('向量维度：{}'.format(query_vec))
print()
print('Query与 Documents的余弦距离：')
for vec in doc_vecs:
    print(cos_sim(query_vec, vec))

print()
print('query 与 Documents 的欧式距离 ：')
for vec in doc_vecs:
    print(l2(query_vec, vec))
