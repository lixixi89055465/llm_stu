from sentence_transformers import CrossEncoder

# model = CrossEncoder('BAAI/bge-reranker-large', max_length=512) # 多语言，国产，模型较大
# model = CrossEncoder('BAAI/bge-reranker-large', max_length=512)  # 多语言，国产，模型较大
model = CrossEncoder(
    model_name='/home/nanji/workspace/bge-reranker-large',
    # local_files_only=True,
    # cache_dir='/home/nanji/workspace/bge-reranker-large'
)
# 定义查询句子和语料库
query = "A man is eating pasta."

corpus = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
]

# 对句子进行排名
ranks = model.rank(query, corpus)
print('Query:', query)

for rank in ranks:
    print(f"{rank['score']:.2f} \t {corpus[rank['corpus_id']]}")

import numpy as np

# 使用 numpy 进行排序
sentence_combinations = [[query, sentence] for sentence in corpus]
scores = model.predict(sentence_combinations)
ranked_indices = np.argsort(scores)
print('Scores:',scores)
print('Indices:',ranked_indices)