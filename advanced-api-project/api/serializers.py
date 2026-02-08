class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Includes nested BookSerializer to display
    all books written by the author.
    """

    # Nested serializer to show related books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'books'
        ]
