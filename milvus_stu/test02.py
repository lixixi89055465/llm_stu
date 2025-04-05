from pymilvus import __version__

import uuid
import numpy as np
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
# total_num = 3000


def generate_uuids(number_of_uuids):
    uuids = [str(uuid.uuid4()) for _ in range(number_of_uuids)]
    return uuids


print('start connecting to Milvus')
connections.connect(
    'default',
    host=host,
    port=port,
    user=username,
    password=password
)
fields = [
    FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name='random', dtype=DataType.DOUBLE),
    FieldSchema(name='comment', dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name='embeddings', dtype=DataType.FLOAT_VECTOR, dim=dim)
]
schema = CollectionSchema(fields, 'hello_milvus is the simplest demo to introduce the APIS!')
print(schema)
print('create collection `hello_world`')
coll = Collection(collection_name, \
                  schema, \
                  consistency_level='Bounded', \
                  shards_num=1)
print('Start inserting `hello_world`')
coll = Collection(collection_name, schema, consistency_level='Bounded', shards_num=1)
print('Start inserting entities')
rng = np.random.default_rng(seed=19530)

entities = [
    [i for i in range(num_entities)],
    rng.random(num_entities).tolist(),
    generate_uuids(num_entities),
    rng.random((num_entities, dim))
]
insert_result = coll.insert(entities)
print('Start flush ')
coll.flush()
print('done')
