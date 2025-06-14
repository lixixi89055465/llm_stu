import json
import os
import warnings

# import pymysql
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, UnstructuredMarkdownLoader, CSVLoader
from langchain_core.documents.base import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_text_splitters import RecursiveJsonSplitter
from pymilvus import MilvusClient, utility, Collection, connections
from tqdm import tqdm
from dotenv import load_dotenv

_ = load_dotenv("/Users/zhulang/work/llm/self_rag/.env")

warnings.filterwarnings("ignore", category=Warning)
base_url = "http://192.168.11.178:11434/v1"


class ChatDoc(object):

    def __init__(self):
        self.loader = {
            ".pdf": PyPDFLoader,
            ".txt": Docx2txtLoader,
            ".docx": Docx2txtLoader,
            ".json": self.handle_json,
            ".md": UnstructuredMarkdownLoader,
            ".csv": CSVLoader,
        }

        self.split_text = []
        # self.model = ChatOpenAI(temperature=0, model="gpt-4o")
        self.model = ChatOpenAI(base_url=base_url, temperature=0, model='qwen2:latest', api_key='empty')

        # llm = ChatOpenAI(model='qwen2:latest', temperature=0,
        #                  base_url=base_url, api_key='empty')

        # self.milvus_client = MilvusClient(db_name="./demo.db", uri="")
        self.milvus_client = MilvusClient(uri="http://localhost:19530", dbname="./milvus_demo.db")
        self.vector_storage()
        # self.mysql_client = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="hhjy2024@Zl.",
        #                                     database="test_ai", charset="utf8")
        # self.cur = self.mysql_client.cursor()

    def handle_json(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = f.read()
            return data

    def is_json(self, str):
        try:
            json.loads(str)
            return True
        except Exception:
            return False

    def get_file(self, filename):
        file_extension = os.path.splitext(filename)[1]
        loader_class = self.loader.get(file_extension, None)
        if loader_class:
            if file_extension == ".json":
                data = loader_class(filename)
            else:
                data = loader_class(filename).load()
            return data
        else:
            return None

    def split_sentences(self, filename):
        full_text = self.get_file(filename)
        if full_text:
            text_splitter = CharacterTextSplitter(chunk_size=210, chunk_overlap=30, add_start_index=True,
                                                  length_function=len)
            json_splitter = RecursiveJsonSplitter(max_chunk_size=210)
            if self.is_json(full_text):
                split_text = json_splitter.split_text(json_data=json.loads(full_text), ensure_ascii=False)
                print(split_text)
            else:
                split_text = text_splitter.split_documents(full_text)
            self.split_text = split_text

    def emb_text(self, text):
        from langchain_ollama import OllamaEmbeddings
        embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        # embedding = OllamaEmbeddings(
        #     model='nomic-embed-text',
        #     base_url=base_url,
            # normalize=True
        # )
        embedding_dim = embedding.embed_query(text)
        return embedding_dim

    def vector_storage(self):
        data_vector = []
        for idx, text in enumerate(tqdm(self.split_text, desc="测试向量数据库")):
            if isinstance(text, Document):
                text = text.page_content
            data_vector.append({"id": idx, "text": text, "vector": self.emb_text(text)})

        self.milvus_client.create_collection(
            collection_name="RAG_vector",
            dimension=1536,
            metric_type="IP",  # Inner product distance
            consistency_level="Strong",  # Strong consistency level
        )
        self.milvus_client.insert(collection_name="RAG_vector", data=data_vector)

    def ask_and_find(self, question):
        # db = self.vector_storage()

        my_expected_name = "RAG_vector"  # 替换成你认为应该存在的名称

        # if utility.has_collection(using='default', collection_name=my_expected_name) == False:
        #     self.milvus_client.create_collection(
        #         collection_name="RAG_vector",
        #         dimension=1536,
        #         metric_type="IP",  # Inner product distance
        #         consistency_level="Strong",  # Strong consistency level
        #     )
        search_result = self.milvus_client.search(
            collection_name="RAG_vector",
            data=[self.emb_text(question)],
            limit=5,
            params={"metric_type": "IP"},
            output_fields=["text"],
        )
        info_result = ""
        for res in search_result[0]:
            info_result += res["entity"]["text"]
        print("调用rag方法")
        # print(info_result)
        return info_result

    def chat_with_doc(self, question):
        contexts = self.ask_and_find(question)
        self.prompt = ChatPromptTemplate.from_messages([HumanMessage(content=f"{question},文档内容:{contexts}")])
        messages = self.prompt.format_messages(context=contexts, question=question)
        res = self.model.stream(messages)
        content = ""
        for i in res:
            content += i.content
        return content

    # def query_data(self, query):
    #     messages = [SystemMessage(content="""你是一位mysql数据的查询工作者，你熟悉mysql的各种表的数据查询语法。现在有一张表的结构是：
    #             CREATE TABLE `camp_package` (
    #               `id` int NOT NULL AUTO_INCREMENT COMMENT '营地产品id',
    #               `product_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '营地的房型名称',
    #               `person_num` int NOT NULL COMMENT '允许入住的最多人数',
    #               `product_area` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '产品面积 单位是平方米',
    #               `product_position` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '产品位置',
    #               `daily_price` decimal(10,2) NOT NULL COMMENT '日常价格 单位是元',
    #               `weekend_price` decimal(10,2) NOT NULL COMMENT '周末价格 单位是元',
    #               `festival_price` decimal(10,2) NOT NULL COMMENT '节日价格  单位是元',
    #               `bottom_price` decimal(10,2) NOT NULL COMMENT '最低价格  单位是元',
    #               PRIMARY KEY (`id`)
    #             ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    #             你需要根据表的结构生成对应的sql语句给到用户，只需要输出纯sql语句，不需要其他任何的前缀或后缀，不需要换行输出，并且把对应产品的详情查询出来。
    #             """)]
    #     messages.append(HumanMessage(content=f"{query}"))
    #     res = self.model.invoke(messages)
    #     sql = res.content.replace("sql", "").strip()
    #     try:
    #         self.cur.execute(f"{sql}")
    #         data = self.cur.fetchall()
    #     except:
    #         data = "未查询到结果或查询结果为空时,请使用RAG的方式再次查询"
    #     print("调用query方法")
    #     return data
