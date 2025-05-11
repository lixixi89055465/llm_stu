# -*- coding: utf-8 -*-
# @Time : 2025/5/10 10:19
# @Author : nanji
# @Site : 
# @File : testTypeDict.py
# @Software: PyCharm 
# @Comment :

from typing import TypedDict


class User(TypedDict):
    name: str
    age: int
    is_active: bool


user: User = {
    'name': 'John Doe',
    'age': 30,
    'is_active': True
}
