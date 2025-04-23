from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

examples = [
    {
        "question": "谁的寿命更长，穆罕默德·阿里还是艾伦·图灵?",
        "answer":
            """
            这里需要跟进问题吗:是的。
            跟进:穆罕默德·阿里去世时多大?
            中间答案:穆罕默德·阿里去世时74岁
            跟进:艾伦·图灵去世时多大?
            中间答案:艾伦·图灵去世时41岁。
            所以最终答案是:穆罕默德·阿里
            """
    },
    {
        "question": "craigslist的创始人是什么时候出生的?",
        "answer":
            """
            这里需要跟进问题吗:是的。
            跟进:craigslist的创始人是谁?
            中间答案:craigslist由Craig Newmark创立。
            跟进:Craig Newmark是什么时候出生的?
            中间答案:Craig Newmark于1952年12月6日出生
            所以最终答案是:1952年12月6日            
            """
    }
]
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
