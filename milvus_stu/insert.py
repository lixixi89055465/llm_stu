import uuid
import numpy as np
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema, DataType,
    Collection
)

collection_name = 'hello_milvus3'
host = '192.168.11.235'
port = 19530
username = ''
password = ''
num_entities, dim = 3000, 3


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

schema = CollectionSchema(
    fields, 'hello_milvus is th simplest demo to introduce the APIS'
)
print('Create collection `hello world`')
coll = Collection(collection_name,
                  schema,
                  consistency_level='Bounded',
                  shards_num=1)
print('Start inserting entites')
rng = np.random.default_rng(seed=19530)
entites = [
    [i for i in range(num_entities)],
    rng.random(num_entities).tolist(),
    generate_uuids(num_entities),
    rng.random((num_entities, dim))
]
insert_result = coll.insert(entites)
print('Start flush')
coll.flush()
print('Start creating index')
index_params = {
    'index_type': 'HNSW',
    'metric_type': 'COSINE',
    'params': {
        'M': 16,
        'efConstruction': 40
    }
}
coll.create_index(
    field_name='embeddings',
    index_params=index_params,
    index_name='idx_em'
)

coll.load()
print('done')

