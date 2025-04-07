from pymilvus import (
    connections,
    Collection
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
coll = Collection(
    collection_name,
    consistency_level='Bounded',
    shards_num=1
)
print('Start creating index')
index_params = {
    'index_type': 'FLAT',
    'metric_type': 'L2',
    'params': {}
}
coll.create_index(
    field_name='embeddings',
    index_params=index_params,
    index_name='idx_em'
)
print('done')
