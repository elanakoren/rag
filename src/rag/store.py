import chromadb

def store_chunks(encoded_dataset: list[dict], collection_name: str = "pg19") -> None:
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name=collection_name)

    # TODO: more robust ID generation
    ids = [f"{record['short_book_title']}-{record['position']}" for record in encoded_dataset]
    embeddings = [record['encoded_chunk'].tolist() for record in encoded_dataset]
    documents = [record['text'] for record in encoded_dataset]
    metadatas = [
        {'short_book_title': record['short_book_title'], 'position': record['position']}
        for record in encoded_dataset
    ]

    batch_size = 5000
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i + batch_size],
            embeddings=embeddings[i:i + batch_size],
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
        )
