from ebooklib import epub

path = input("Path to EPUB file: ")
book = epub.read_epub(path)

print("Title:", book.get_metadata('DC', 'title'))
print("Spine length:", len(book.spine))
print()

first_id, _ = book.spine[0]
first_item = book.get_item_with_id(first_id)
print("First spine entry id:", first_id)
print("First item type:", type(first_item))
print("First item content (first 500 chars):")
print(first_item.get_content()[:500])
