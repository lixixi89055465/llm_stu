from langchain_community.llms import Ollama
from flask_api.RAG.config import base_url
import warnings

warnings.filterwarnings('ignore', category=Warning)
llm = Ollama(base_url=base_url, mode='qwen2.72b', temperature=0.6)
res = llm.invoke('你是谁?')
print(res)
