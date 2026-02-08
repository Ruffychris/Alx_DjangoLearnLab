from rest_framework import serializers
from datetime import datetime

from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Converts Book model instances into JSON format
    and validates incoming book data.
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        """
        Ensures that the publication year is not in the future.

        Prevents users from submitting unrealistic dates.
        """

        current_year = datetime.now().year

        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )

        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Includes nested BookSerializer to display
    all books written by the author.
    """

    # Nested serializer to show related books
    books = BookSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'books'
        ]
