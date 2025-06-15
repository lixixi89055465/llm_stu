# -*- coding: utf-8 -*-
# @Time : 2025/6/15 21:52
# @Author : nanji
# @Site : 
# @File : test03.py
# @Software: PyCharm 
# @Comment :

conditional_map = {
    "get_location_agent": "get_location_agent",
    "search_around_agent": "search_around_agent",
    "rag_agent": "rag_agent",
    "FINISH": 'END',
}
a = lambda x, y: x, conditional_map.items()
print(a)
