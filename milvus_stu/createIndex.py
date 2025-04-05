from pymilvus import Collection
from pymilvus import (
    connections,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

collection_name = 'hello_milvus1'
host = '192.168.11.235'
port = 19530
username = ''
password = ''
num_entities, dim = 1000, 128
# collection = Collection('hello_milvus1')
connections.connect(
    'default',
    host=host,
    port=port,
    user=username,
    password=password
)

coll = Collection(collection_name)

index_params = {
    "index_type": "AUTOINDEX",
    "metric_type": "L2",
    "params": {}
}

coll.create_index(
  field_name="embeddings",
  index_params=index_params,
  index_name="idx_em"
)