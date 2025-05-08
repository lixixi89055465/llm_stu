import os

os.environ[
    'USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools.retriever import create_retriever_tool

# os.environ['TAVILY_API_KEY'] = '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'
from langchain_community.tools.tavily_search import TavilySearchResults
import os

os.environ['TAVILY_API_KEY'] = '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'

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ['OPENAI_API_KEY'] = 'hk-v3x5ll1000053052cb6ee2d41a9e5c4e0dbbb349026580e3'
os.environ['OPENAI_BASE_URL'] = 'https://api.openai-hk.com/v1'
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import \
    WebBaseLoader  # USER_AGENT environment variable not set, consider setting it to identify your requests.

loader = WebBaseLoader('https://baike.baidu.com/item/%E7%8C%AB/22261')
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    # chunk_size 参数在 RecursiveCharacterTextSplitter中用于指定每个文档快的最大字符数。他的作用主要有一下作用。
    # chunk_overlap 参数用于指定每个文档快之间的重叠字符数。这意味着，当文档被拆分成较小的快时，每个块的末尾部分都会与下一个快的开头部分重叠
    # 第一个快包含字符1到1000.第二个块包含字符 801,到1800.第三个快包含字符1601到2600
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)

vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()
print(retriever.invoke('猫的特征')[0])
retriever_tool = create_retriever_tool(
    retriever,
    'wiki_search',
    '搜索维基百科',
)

model = ChatOpenAI(model='gpt-4')
search = TavilySearchResults(max_results=1)
tools = [search, retriever_tool]
from langchain import hub

# 获取要使用的提示 - 您可以修改这个
prompt = hub.pull('hwchase17/openai-functions-agent')
print(prompt.messages)
from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(model, tools, prompt)

from langchain.agents import AgentExecutor

# agent_executor = AgentExecutor(agent=agent, tools=tools)
# print(agent_executor.invoke({'input': '猫的特征?今天上海天气怎么样?'}))
# from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools)
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)
response = agent_with_chat_history.invoke(
    {'input': 'Hi.我的名字是Jack'},
    config={'configurable': {'session_id': '123'}}
)
print(response)

response = agent_with_chat_history.invoke(
    {'input': '我叫什么名字?'},
    config={'configurable': {'session_id': "123"}}
)
print(response)
response = agent_with_chat_history.invoke(
    {'input': '我叫什么名字？'},
    config={'configurable': {'session_id': "456"}}
)
print(response)

'''
page_content='[17]。猫共有26种独特面部动作，包括瞳孔放大或收缩、舔鼻子、延长或缩回胡须、不同的耳朵位置等，而每个表情都结合运用了大约4种面部动作 [17]。体态体型猫体型小，体色由蓝灰色到棕黄色，体型瘦削，身长0.3-0.5米，全身毛被密而柔软，锁骨小，吻部短，眼睛圆，颈部粗壮，四肢较短，足下有数个球形肉垫；舌面被有角质层的丝状钩形乳突。猫雌雄性个体彼此相似，仅雄性头部粗圆，个体大些。 [8]有黄、黑、白、灰等各种毛色；身形像狸，外貌像老虎，毛柔而齿利（有几乎无毛的品种）。以尾长腰短，目光如金银，上腭棱多的最好。猫的身体分为头、颈、躯干、四肢和尾五部分，大多数部位披毛，少数为无毛猫。猫的趾底有脂肪质肉垫，因而行走无声，捕鼠时不会惊跑鼠，趾端生有锐利的趾甲。爪能够缩进和伸出。猫在休息和行走时爪缩进去，只在捕鼠和攀爬时伸出来，防止趾甲被磨钝。猫的前肢有五趾，后肢有四趾。猫的牙齿分为门齿、犬齿和臼齿。犬齿特别发达，尖锐如锥，适于咬死捕到的鼠类，臼齿的咀嚼面有尖锐的突起，适于把肉嚼碎；门齿不发达。中国常见的猫黑猫黑猫奶牛猫奶牛猫白猫白猫橘猫橘猫三花猫三花猫玳瑁猫玳瑁猫狸花猫狸花猫四川简州猫四川简州猫山东狮子猫山东狮子猫猫还能从它的牙齿来判断它的年龄成年猫咪的牙齿共30枚。幼年猫咪的牙齿共26枚。猫的牙齿从两边往中间分别是：上排——臼齿大臼齿前臼齿犬齿6颗门齿下排——大臼齿前臼齿犬齿6颗门齿14天左右开始长牙2～3周龄乳门牙长齐。近两月龄时，乳牙全部长齐，呈白色，细而尖3～4月龄更换第一乳门牙5～6月龄换第二三乳门齿及乳犬牙6月龄以后全部换上恒齿8月龄恒齿长齐，洁白光亮，门齿上部有尖凸1岁下颌第二门齿大尖峰，磨损至小尖峰平齐，此现象称为尖峰磨灭2岁下颌第二门齿尖峰磨灭3岁上颌第一门齿尖峰磨灭4岁上颌第二门齿尖峰磨灭5岁下颌第三门齿尖峰稍磨损，下颌第一二门齿磨损面为矩形5.5岁下颌第三齿尖磨灭，犬齿钝圆6.5岁下颌第一门齿磨损至齿根部，磨损面为纵椭圆形7.5岁下颌第一门齿磨损面向前方倾斜8.5岁下颌第二及上颌第一门齿磨损面呈纵椭圆形9～16岁门齿脱落犬齿不齐生活习性播报编辑猫不喜群居，有领地观念，一旦遭到入侵便会发起攻击，且有极高的攀爬本领。' metadata={'source': 'https://baike.baidu.com/item/%E7%8C%AB/22261', 'title': '猫（猫科猫属动物）_百度百科', 'description': '猫（拉丁学名：Felis silvestris catus），是食肉目猫科猫属的脊索动物。猫体型小，体色由蓝灰色到棕黄色，体型瘦削，身长0.3-0.5米，全身毛被密而柔软，锁骨小，吻部短，眼睛圆，颈部粗壮，四肢较短，足下有数个球形肉垫；舌面被有角质层的丝状钩形乳突。猫雌雄性个体彼此相似，仅雄性头部粗圆，个体大些。猫的繁殖与生育期长达一生，寿命有12-17年。据宋朝陆游《嘲畜猫》诗自注：“俗言猫为虎舅，教虎百为，惟不教上树”。故别称“虎舅”。猫分布范围广泛，从热带雨林、沙漠荒丘到寒冷的草原和高原，可以分布在除南极洲以外的每一个大陆上。猫不喜群居，有领地观念，一旦遭到入侵便会发起攻击，且有极高的攀爬本领。猫为肉食性动物，野外靠捕食鼠、鸟、鱼等小动物为生，喜食荤腥，有偏食的特点。猫作为家庭宠物，可以缓解人们的心理压力、满足人们的情感需求。且就其捕捉老鼠一项，每年就能为人类挽回巨额的经济损失。猫文', 'language': 'No language found.'}
[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='You are a helpful assistant'), additional_kwargs={}), MessagesPlaceholder(variable_name='chat_history', optional=True), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='{input}'), additional_kwargs={}), MessagesPlaceholder(variable_name='agent_scratchpad')]
{'input': 'Hi.我的名字是Jack', 'chat_history': [], 'output': '你好，Jack。很高兴遇到你。我可以帮助你做什么呢？'}
{'input': '我叫什么名字?', 'chat_history': [HumanMessage(content='Hi.我的名字是Jack', additional_kwargs={}, response_metadata={}), AIMessage(content='你好，Jack。很高兴遇到你。我可以帮助你做什么呢？', additional_kwargs={}, response_metadata={})], 'output': '你的名字是Jack。'}
{'input': '我叫什么名字？', 'chat_history': [], 'output': '抱歉，我无法查看您的个人信息，包括您的姓名。您可以告诉我您的名字，我将用于称呼您。'}


'''