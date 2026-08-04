from bs4 import BeautifulSoup
from ebooklib import epub

def parse_epub(path: str) -> dict:
    book = epub.read_epub(path)
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
