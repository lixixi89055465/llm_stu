# -*- coding: utf-8 -*-
# @Time    : 2024/11/11 下午10:45
# @Author  : nanji
# @Site    : 
# @File    : testJson.py
# @Software: PyCharm 
# @Comment :https://blog.csdn.net/Lingoesforstudy/article/details/143504078
import json

json_str = '{"name": "Alice", "age": 25}'
data = json.loads(json_str)
print(data['name'])
