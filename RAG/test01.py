# 使用 modelscope 提供的 sdk 进行模型下载
from modelscope import snapshot_download

# model_id 模型的id
# cache_dir 缓存到本地的路径
# model_dir = snapshot_download(model_id="BAAI/bge-base-zh-v1.5", cache_dir="D:/AIProject/modelscope")
model_dir = snapshot_download(model_id="BAAI/bge-base-zh-v1.5")
model_dir = snapshot_download(model_id="Qwen/Qwen2.5-7B-Instruct")

import logging
import sys
import torch
from llama_index.core import PromptTemplate, Settings, SimpleDirectoryReader, VectorStoreIndex, load_index_from_storage, \
    StorageContext, QueryBundle
from llama_index.core.schema import MetadataMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.node_parser import SentenceSplitter

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
SYSTEM_PROMPT = """You are a helpful AI assistant."""
query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
)
llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=2048,
    generate_kwargs={"temperature": 0.0, "do_sample": False},
    query_wrapper_prompt=query_wrapper_prompt,
    # tokenizer_name='D:/AIProject/modelscope/Qwen/Qwen2___5-7B-Instruct',
    # model_name='D:/AIProject/modelscope/Qwen/Qwen2___5-7B-Instruct',
    tokenizer_name='/home/nanji/.cache/modelscope/hub/models/Qwen/Qwen2___5-7B-Instruct',
    model_name='/home/nanji/.cache/modelscope/hub/models/Qwen/Qwen2___5-7B-Instruct',
    device_map="auto",
    model_kwargs={"torch_dtype": torch.float16},
)
Settings.llm = llm
# 使用 llama_index_embeddings_huggingface 调用本地 embedding 模型
Settings.embed_model = HuggingFaceEmbedding(
    model_name='/home/nanji/.cache/modelscope/hub/models/BAAI/bge-base-zh-v1___5'
)
# 读取文档
# documents = SimpleDirectoryReader(
#     './data',
#     # required_exts=['.txt']
# ).load_data()

# 对文档进行切分，将切分后的片段转化为embedding向量，构建向量索引
# index = VectorStoreIndex.from_documents(
#     documents,
#     transformations=[SentenceSplitter(chunk_size=256)]
# )

# SentenceSplitter 参数详细设置：
# 构建查询引擎
# query_engine = index.as_query_engine(similarity_top_k=5)
# response = query_engine.query('不耐疲劳，口燥、咽干可能是哪些证候？')
# print(response)
#
# 讲 embedding 向量和向量索引存储到文件中
# index.storage_context.persist(persist_dir='./doc_emb')
# 很方便的集成目前主流的向量数据库 chroma

# 从存储文件中读取 embedding 向量和向量索引
storage_context = StorageContext.from_defaults(
    persist_dir='doc_emb'
)
# 根据存储的 embedding 向量和向量索引重新构建检索索引
index = load_index_from_storage(storage_context)
# 构建查询索引
query_engine = index.as_query_engine(similarity_top_k=5)
# 获取我们抽取出的相似度 top 5 的片段
contexts = query_engine.retrieve(
    QueryBundle(
        '不耐疲劳，口燥、咽干可能是那些症候？'
    )
)
print('-' * 10 + 'ref' + '-' * 10)
for i, context in enumerate(contexts):
    print('*' * 10 + f'chunk {i} start ' + '*' * 10)
    content = context.node.get_content(metadata_mode=MetadataMode.LLM)
    print(content)
    print('*' * 10 + f'chunk {i} end ' + '*' * 10)
print('-' * 10 + 'ref' + '-' * 10)
# 查询获得答案
response = query_engine.query(
    '不耐疲劳，口燥、咽干可能是那些症候?'
)
print(response)
# 从存储文件中读取 embedding向量和向量索引
storage_context = StorageContext.from_defaults(
    persist_dir='doc_emb'
)
# 根据存储的 embedding向量和向量索引重新构建检索索引
index = load_index_from_storage(storage_context)
# 构建查询引擎
query_engine = index.as_query_engine(similarity_top_k=5)
# 获取我们抽取出的相似度 top 5 的片段
contexts = query_engine.retrieve(
    QueryBundle('不耐疲劳，口燥、咽干可能是哪些症候？')
)
print('-' * 10 + 'ref' + '-' * 10)
for i, context in enumerate(contexts):
    print('*' * 10 + f'chunk {i} start ' + '*' * 10)
    content = context.node.get_content(metadata_mode=MetadataMode.LLM)
    print(content)
    print('*' * 10 + f'chunk {i} end ' + '*' * 10)
print('-' * 10 + 'ref' + '-' * 10)

# 查询获得答案
resposne = query_engine.query(
    '不耐疲劳，口燥、咽干可能是哪些症候？'
)
print(resposne)
