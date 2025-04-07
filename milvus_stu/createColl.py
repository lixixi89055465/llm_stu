from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection
)

collection_name = 'hello_milvus2'
host = '192.168.11.235'
port = 19530
username = ''
password = ''
num_entities, dim = 5000, 3

print('start 4 connection to Milvus ')
connections.connect(
    'default',
    host=host,
    port=port,
    user=username,
    password=password
)
fields = [
    FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, password=password),
    FieldSchema(name='random', dtype=DataType.DOUBLE),
    FieldSchema(name='comment', dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name='embeddings', dtype=DataType.FLOAT_VECTOR, dim=dim)
]
schema = CollectionSchema(fields, 'hello 4 milvus is the simples demo to introve the apis')
print('create collection `hello world`')
coll = Collection(collection_name, schema, consistency_level='Bounded', shards_num=1)

print('done')
