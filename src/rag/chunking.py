def chunk_text(book: dict, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    chunks = []
    start = 0
    text = book['text']
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        # avoid cutting a word in half
        while end < n and not text[end].isspace():
            end += 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({'short_book_title': book['short_book_title'], 'text': chunk, 'position': start})
        if end >= n:
            break
        start = end - overlap
    return chunks
