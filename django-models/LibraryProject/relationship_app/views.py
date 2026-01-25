from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library, Book

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Book

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

from django.shortcuts import render
from .models import Book

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


def list_books(request):
    return render(
        request,
        'relationship_app/list_books.html',
        {'books': Book.objects.all()}
    )


def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'


def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'


def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')



# Add Book View
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            from .models import Author
            author = Author.objects.get(id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')


# Edit Book View
@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            book.title = title
            book.save()
            return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'book': book})


# Delete Book View
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
