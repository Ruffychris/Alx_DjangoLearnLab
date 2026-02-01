from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import ExampleForm  # <-- must exist exactly like this

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    form = ExampleForm(request.POST or None)  # use ExampleForm here
    if form.is_valid():
        book = form.save(commit=False)
        book.created_by = request.user
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'form': form})

# other views (edit, delete, list) remain the same
