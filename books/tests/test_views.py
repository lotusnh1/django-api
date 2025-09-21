from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import Book
from .serializers import BookSerializer

from dotenv import load_dotenv
import os

# Load .env file for the test environment
load_dotenv()

class BookListCreateViewIntegrationTestCase(TestCase):

    def setUp(self):
        # Create a few book objects in the database to test the list view
        self.book1 = Book.objects.create(title="Book 1", author="Author 1", published_date="2023-01-01")
        self.book2 = Book.objects.create(title="Book 2", author="Author 2", published_date="2023-02-01")
        self.url = '/books/'  # URL for the BookListCreateView

    def test_integration_get_books(self):
        # Test GET request for a list of books and validate the integration of the database with the API
        client = APIClient()
        response = client.get(self.url)

        # Verify status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the books returned match the database entries
        books = Book.objects.all()
        serialized_books = BookSerializer(books, many=True).data
        self.assertEqual(response.data, serialized_books)

    def test_integration_create_book(self):
        # Test POST request for creating a new book and validate the integration with the database
        client = APIClient()
        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'published_date': '2023-09-21'
        }

        # Send the POST request
        response = client.post(self.url, new_book_data, format='json')

        # Verify status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the database to ensure the new book was saved
        book = Book.objects.get(title='New Book')
        self.assertEqual(book.author, 'New Author')
        self.assertEqual(book.published_date.strftime('%Y-%m-%d'), '2023-09-21')

        # Verify the response content matches the created book
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['author'], 'New Author')
        self.assertEqual(response.data['published_date'], '2023-09-21')
