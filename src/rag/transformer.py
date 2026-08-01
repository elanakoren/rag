from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def encode(sentences):
    embeddings = model.encode(sentences)
    return embeddings
