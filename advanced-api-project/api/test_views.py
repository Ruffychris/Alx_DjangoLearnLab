from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        
        # Create test books
        self.book1 = Book.objects.create(title='Book One', publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title='Book Two', publication_year=2010, author=self.author2)

    # ---------------------------
    # TEST LIST AND DETAIL VIEWS
    # ---------------------------
    def test_book_list_view(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_book_detail_view(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # ---------------------------
    # TEST CREATE VIEW
    # ---------------------------
    def test_book_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-create')
        data = {
            'title': 'Book Three',
            'publication_year': 2022,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title='Book Three').author.name, 'Author One')

    def test_book_create_view_unauthenticated(self):
        url = reverse('book-create')
        data = {
            'title': 'Book Four',
            'publication_year': 2023,
            'author': self.author2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------------
    # TEST UPDATE VIEW
    # ---------------------------
    def test_book_update_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-update', args=[self.book1.id])
        data = {'title': 'Updated Book One'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')

    def test_book_update_view_unauthenticated(self):
        url = reverse('book-update', args=[self.book2.id])
        data = {'title': 'Hacked Book'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------------
    # TEST DELETE VIEW
    # ---------------------------
    def test_book_delete_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_book_delete_view_unauthenticated(self):
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------------
    # TEST FILTERING, SEARCHING, ORDERING
    # ---------------------------
    def test_book_filtering(self):
        url = reverse('book-list') + f'?author__name={self.author1.name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.id)

    def test_book_searching(self):
        url = reverse('book-list') + '?search=Book Two'
        response = self.client.get(url)
