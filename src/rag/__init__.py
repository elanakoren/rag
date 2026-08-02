from datasets import load_dataset
from rag.chunking import chunk_text
from rag.transformer import encode
from rag.store import store_chunks
import chromadb

def main() -> None:
    question = input("Ask a question: ")
    client = chromadb.PersistentClient(path="./chroma_db")
    encoded_question = encode(question)
    ds = load_dataset("emozilla/pg19", split="train[:50]")
    chunked_text = []
    encoded_dataset = []
    for text in ds:
        chunked_text.extend(chunk_text(text))

    # TODO: Batch for performance
    for chunk in chunked_text:
        encoded_chunk = encode(chunk['text'])
        encoded_dataset.append({
            'encoded_chunk': encoded_chunk,
            'text': chunk['text'],
            'short_book_title': chunk['short_book_title'],
            'position': chunk['position'],
            })
    store_chunks(encoded_dataset)
    collection = client.get_collection(name='pg19')
    result = collection.query(query_embeddings=[encoded_question], n_results=5)
