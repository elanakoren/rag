def format_result(result) -> list[dict]:
    documents = result['documents'][0]
    metadatas = result['metadatas'][0]
    return [
        {
            'text': document,
            'short_book_title': metadata['short_book_title'],
            'position': metadata['position'],
        }
        for document, metadata in zip(documents, metadatas)
    ]
