from datasets import load_dataset
from rag.chunking import chunk_text
from rag.transformer import encode

def main() -> None:
    ds = load_dataset("emozilla/pg19", split="train[:50]")
    chunked_text = []
    encoded_dataset = []
    for text in ds:
        chunked_text.extend(chunk_text(text))
    for chunk in chunked_text:
        encoded_chunk = encode(chunk['text'])
        encoded_dataset.append({
            'encoded_chunk': encoded_chunk,
            'text': chunk['text'],
            'short_book_title': chunk['short_book_title'],
            'position': chunk['position'],
            })
    print(encoded_dataset[0])