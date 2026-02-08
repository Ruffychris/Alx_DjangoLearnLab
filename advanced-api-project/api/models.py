from django.db import models


class Author(models.Model):
    """
    Represents a book author.

    This model stores basic information about authors.
    Each author can be linked to multiple books
    (one-to-many relationship).
    """

    name = models.CharField(
        max_length=100,
        help_text="Full name of the author"
    )

    def __str__(self):
        """
        Returns a readable representation of the author.
        Used in Django admin and shell.
        """
        return self.name


class Book(models.Model):
    """
    Represents a book written by an author.

    Each book is linked to exactly one author
    through a foreign key relationship.
    """

    title = models.CharField(
        max_length=200,
        help_text="Title of the book"
    )

    publication_year = models.IntegerField(
        help_text="Year the book was published"
    )

    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE,
        help_text="Author who wrote this book"
    )

    def __str__(self):
        """
        Returns the book title for display purposes.
        """
        return self.title
