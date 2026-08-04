from rag.chunking import chunk_text
from rag.transformer import encode
from rag.store import store_chunks
from rag.format import format_result, citation_string, citation_key
from rag.api import call_claude
from rag.epub import parse_epub
from rag.library import list_books, add_book
import chromadb

def index() -> None:
    path = input("Path to EPUB file: ")
    try:
        book = parse_epub(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return
    chunked_text = chunk_text(book)

    encoded_dataset = []
    # TODO: Batch for performance
    for chunk in chunked_text:
        encoded_chunk = encode(chunk['text'])
        encoded_dataset.append({
            'encoded_chunk': encoded_chunk,
            'text': chunk['text'],
            'short_book_title': chunk['short_book_title'],
            'position': chunk['position'],
            'percentage': chunk['percentage'],
            })
    store_chunks(encoded_dataset)
    add_book(book['short_book_title'])

def main() -> None:
    books = list_books()
    if not books:
        print("No books indexed yet. Run 'rag-index' first.")
        return

    if len(books) == 1:
        book_title = books[0]
    else:
        print("Which book are you asking about?")
        for i, title in enumerate(books, start=1):
            print(f"{i}. {title}")
        while True:
            choice = input("> ")
            if choice.isdigit() and 1 <= int(choice) <= len(books):
                book_title = books[int(choice) - 1]
                break
            print(f"Please enter a number between 1 and {len(books)}.")

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name='library')
    while True:
        question = input("Ask a question (or 'quit' to exit): ")
        if question.strip().lower() in ('quit', 'exit', 'q'):
            break
        encoded_question = encode(question)
        result = collection.query(
            query_embeddings=[encoded_question.tolist()],
            n_results=5,
            where={"short_book_title": book_title},
        )
        excerpts = format_result(result)
        citation_string_result = citation_string(excerpts)
        answer = call_claude(citation_string_result, question)
        print(answer)
        print()
        print("Sources:")
        print(citation_key(excerpts))
        print()
