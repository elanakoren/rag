from rag.epub import parse_epub

path = input("Path to EPUB file: ")
result = parse_epub(path)

print("Title:", result['short_book_title'])
print("Total length:", len(result['text']))
print()
print(result['text'][:2000])
