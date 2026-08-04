import json
from pathlib import Path

LIBRARY_PATH = Path("library.json")

def list_books() -> list[str]:
    if not LIBRARY_PATH.exists():
        return []
    return json.loads(LIBRARY_PATH.read_text())

def add_book(title: str) -> None:
    books = list_books()
    if title not in books:
        books.append(title)
        LIBRARY_PATH.write_text(json.dumps(books))
