# -*- coding: utf-8 -*-
# @Time : 2025/5/29 21:22
# @Author : nanji
# @Site : 
# @File : testType01.py
# @Software: PyCharm 
# @Comment :

def greeting(name: str) -> str:
    return 'Hello' + name


from typing import List

Vector = List[float]


def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]


from typing import Dict, Tuple, Sequence

ConnectionOptions = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[Address, ConnectionOptions]


def broadcast_message(message: str, server: Sequence[Server]) -> None:
    pass


def broadcast_message2(
        message: str,
        servers: Sequence[Tuple[Tuple[str, int], Dict[str, str]]]) -> None:
    pass


from typing import NewType

UserId = NewType('UserId', int)


def get_user_name(user_id: UserId) -> str:
    pass


# 可以通过类型检查
# New Type 实现代码
def NewType(name, tp):
    def new_type(x):
        return x

    new_type.__name__ = name
    new_type.__supertype__ = tp
    return new_type


user_id_1 = UserId(23)
user_id_2 = UserId(46)
a = user_id_1 + user_id_2
print(a)


def get_num(num: int) -> int:
    return num


# 可以通过类型检查
get_num(1)
