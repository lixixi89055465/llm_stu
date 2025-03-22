from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("/home/nanji/workspace/all-MiniLM-L6-v2")

sentences1 = [
    "The new movie is awesome",
    "The cat sits outside",
    "A man is playing guitar",
]
sentences2 = [
    "The dog plays in the garden",
    "The new movie is so great",
    "A woman watches TV",
]
embeddings1 = model.encode(sentences1)
embeddings2 = model.encode(sentences2)
similarities = model.similarity(
    embeddings1, embeddings2
)
for idx_i, sentence1 in enumerate(sentences1):
    print(sentence1)
    for idx_j, sentence2 in enumerate(sentences2):
        print(f'-{sentence2:<30}:{similarities[idx_i][idx_j]:.4f}')

from sentence_transformers import SentenceTransformer, SimilarityFunction

model = SentenceTransformer(
    model_name_or_path="/home/nanji/workspace/all-MiniLM-L6-v2",
    similarity_fn_name=SimilarityFunction.DOT_PRODUCT
)

from sentence_transformers import SentenceTransformerTrainer, SimilarityFunction

model = SentenceTransformer(
    model_name_or_path="/home/nanji/workspace/all-MiniLM-L6-v2",
)
model.similarity_fn_name = SimilarityFunction.DOT_PRODUCT

from sentence_transformers import SentenceTransformer, SimilarityFunction

model = SentenceTransformer(
    model_name_or_path="/home/nanji/workspace/all-MiniLM-L6-v2",
)
sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]
embeddings = model.encode(sentences)
similarities = model.similarity(embeddings, embeddings)
print(similarities)

print('1' * 100)
model.similarity_fn_name = SimilarityFunction.MANHATTAN
print(model.similarity_fn_name)
similarities = model.similarity(embeddings, embeddings)
print(similarities)

import torch
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer(
    model_name_or_path="/home/nanji/workspace/all-MiniLM-L6-v2",
)
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
corpus_embeddings = embedder.encode(
    corpus,
    convert_to_tensor=True
)
queries = [
    "A man is eating pasta.",
    "Someone in a gorilla costume is playing a set of drums.",
    "A cheetah chases prey on across a field.",
]
top_k = min(5, len(corpus))

for query in queries:
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    similarity_scores = embedder.similarity(
        query_embedding,
        corpus_embeddings)[0]
    scores, indices = torch.topk(similarity_scores, k=top_k)
    print('\n Query', query)
    print('Top 5 most similar sentences in corpus:')
    for score, idx in zip(scores, indices):
        print(corpus[idx], f'(score:{score:.4f})')

print('2' * 100)
from sentence_transformers import SentenceTransformerTrainer

model = SentenceTransformer(
    '/home/nanji/workspace/multi-qa-mpnet-base-dot-v1')
docs = [
    "My first paragraph. That contains information",
    "Python is a programming language.",
]
document_embeddings = model.encode(docs)
print('document_embeddings:', document_embeddings)
query = 'What is python'
query_embeddings = model.encode(query)
print('query_embedding:', query_embedding)
