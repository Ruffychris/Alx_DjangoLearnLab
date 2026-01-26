# Retrieve Book Record

from bookshelf.models import Book

# Retrieve the book using objects.get
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year