from pymilvus import (
    connections, db
)

collection_name = 'hello_milvus'
host = '192.168.11.235'
port = 19530
username = ''
password = ''

print('start connecting to milvus')
connections.connect(
    'default',
    host=host,
    port=port,
    user=username,
    password=password
)
# 创建数据库
# database = db.create_database('book')
db.using_database('book')
print('0' * 100)
print(db.list_database())
print('done')
