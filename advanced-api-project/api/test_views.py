from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Author, Book

class BookAPITest(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='king', password='king')
        # create an author to reference in POST data
        self.author = Author.objects.create(name='Initial Author')

        # Create an author and a book
        self.author = Author.objects.create(name='J.K. Rowling')
        self.book = Book.objects.create(
            title='Original Title',
            publication_year=2020,
            author=self.author)

    def test_list(self):
        url = reverse("books")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_list(self):
        url = reverse("books-create")
        # use the serializer's write-only `author_id` field
        data = {'title': 'The Beginning', 'publication_year': 2025, 'author_id': self.author.id}

        self.client.force_login(self.user)  # ✅ Login properly
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        url = reverse('books-update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Updated Title',
            'publication_year': 2021,
            'author_id': self.author.id
        }

        # PATCH request (partial update)
        self.client.force_login(self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.publication_year, 2021)