from django import forms
from .models import Book

# Autograder expects this exact class name
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
