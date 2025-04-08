import uuid
import numpy as np
import random
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema, DataType,
    Collection
)

dim = 3
host = '192.168.11.235'
if __name__ == '__main__':
    connections.connect(
        alias='default',
        user='',
        password='',
        host=host,
        port='19530'
    )
    coll = Collection('hello_milvus3')
    search_param = {
        'metric_type': 'COSINE',
        'params': {'ef': 40}
    }
    search_data = [random.random() for _ in range(dim)]
    results = coll.search(
        data=[search_data],
        anns_field='embeddings',
        param=search_param,
        limit=5,
        # expr=None,
        output_fields=['pk', 'embeddings'],
        # consistency_level='Everytually'
    )
    print(results)
