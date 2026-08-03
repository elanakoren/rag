from datasets import load_dataset
from rag.chunking import chunk_text
from rag.transformer import encode
from rag.store import store_chunks
from rag.format import format_result, citation_string, citation_key
from rag.api import call_claude
from pprint import pprint
import chromadb

def index() -> None:
    ds = load_dataset("emozilla/pg19", split="train[:50]")
    chunked_text = []
    for text in ds:
        chunked_text.extend(chunk_text(text))

    encoded_dataset = []
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

def main() -> None:
    question = input("Ask a question: ")
    encoded_question = encode(question)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name='pg19')
    result = collection.query(query_embeddings=[encoded_question.tolist()], n_results=5)
    excerpts = format_result(result)
    citation_string_result = citation_string(excerpts)
    answer = call_claude(citation_string_result, question)
    print(answer)
    print()
    print("Sources:")
    print(citation_key(excerpts))
