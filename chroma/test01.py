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
    lines = full_text.split("\n")
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' ' + text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


paragraphs = extract_text_from_pdf(
    "llama2.pdf",
    page_numbers=[2, 3],
    min_line_length=10
)
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


# 创建一个向量数据库对象
vector_db = MyVectorDBConnector(
    'demo',
    get_embeddings
)
# 向向量数据库中添加文档
vector_db.add_document(paragraphs)
