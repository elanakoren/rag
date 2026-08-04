def format_result(result) -> list[dict]:
    documents = result['documents'][0]
    metadatas = result['metadatas'][0]
    return [
        {
            'text': document,
            'short_book_title': metadata['short_book_title'],
            'position': metadata['position'],
            'percentage': metadata['percentage'],
        }
        for document, metadata in zip(documents, metadatas)
    ]

def citation_string(excerpts) -> str:
    citation_result = ''
    for i, excerpt in enumerate(excerpts, start=1):
        citation_result += f"[{i}] ({excerpt['short_book_title']}) \"{excerpt['text']}\"\n\n"
    return citation_result

def citation_key(excerpts) -> str:
    lines = [
        f"[{i}] {excerpt['short_book_title']}, {excerpt['percentage']:.1f}% through"
        for i, excerpt in enumerate(excerpts, start=1)
    ]
    return '\n'.join(lines)
