# -*- coding: utf-8 -*-
# @Time : 2025/4/25 0:00
# @Author : nanji
# @Site :  https://www.bilibili.com/video/BV12iQBYWEx9/?spm_id_from=333.788.player.switch&vd_source=50305204d8a1be81f31d861b12d4d5cf&p=5
# @File : chat_history_memory.py
# @Software: PyCharm 
# @Comment :

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
# 引入消息历史记录
