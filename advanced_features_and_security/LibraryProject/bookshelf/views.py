from django.shortcuts import render
from .models import Book
from .forms import BookForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():  # Input is validated here
        book = form.save(commit=False)
        book.created_by = request.user
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def search_books(request):
    query = request.GET.get('q', '')
    # Use ORM safely; no string formatting
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})


# All form handling uses CSRF tokens and Django forms to prevent XSS and SQL injection
# User input is validated via forms and safe ORM queries