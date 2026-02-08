from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# List all books (read-only for unauthenticated users)
class BookListView(generics.ListAPIView):
    """
    Returns a list of all books.
    Read-only access for unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read

# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves details of a single book by its primary key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read

# Create a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book instance.
    Only authenticated users can perform this action.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Update an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book instance.
    Only authenticated users can perform this action.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Delete a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a book instance.
    Only authenticated users can perform this action.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
