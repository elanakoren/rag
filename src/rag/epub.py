from pathlib import Path
from bs4 import BeautifulSoup
from ebooklib import epub

def parse_epub(path: str) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"No file found at '{path}'")
    if file_path.suffix.lower() != '.epub':
        raise ValueError(f"'{path}' doesn't look like an EPUB file (expected a .epub extension)")

    try:
        book = epub.read_epub(path)
    except Exception as e:
        raise ValueError(f"Could not parse '{path}' as an EPUB file: {e}")

    title = book.get_metadata('DC', 'title')[0][0]

    chapters = []
    for idref, _ in book.spine:
        item = book.get_item_with_id(idref)
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        chapters.append(soup.get_text())

    return {
        'text': '\n\n'.join(chapters),
        'short_book_title': title,
    }
