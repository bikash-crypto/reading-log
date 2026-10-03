from django.test import TestCase
from django.urls import reverse

from .models import Author, Book


class LibraryViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name='Mary Shelley', country='United Kingdom')
        cls.book = Book.objects.create(
            title='Frankenstein', author=cls.author, pages=280, status='reading',
        )

    def test_shelf_lists_books(self):
        response = self.client.get(reverse('library:book_list'))
        self.assertContains(response, 'Frankenstein')

    def test_status_filter(self):
        response = self.client.get(reverse('library:book_list'), {'status': 'finished'})
        self.assertNotContains(response, 'spine-title">Frankenstein')

    def test_search(self):
        response = self.client.get(reverse('library:book_list'), {'q': 'shelley'})
        self.assertContains(response, 'Frankenstein')
        response = self.client.get(reverse('library:book_list'), {'q': 'tolstoy'})
        self.assertContains(response, 'No books match')

    def test_book_detail(self):
        response = self.client.get(self.book.get_absolute_url())
        self.assertContains(response, 'Reading now')

    def test_create_book(self):
        response = self.client.post(reverse('library:book_create'), {
            'title': 'The Last Man', 'author': self.author.pk,
            'status': 'want', 'cover': 'navy',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='The Last Man').exists())

    def test_finish_date_before_start_is_rejected(self):
        response = self.client.post(reverse('library:book_create'), {
            'title': 'Bad dates', 'author': self.author.pk, 'status': 'finished',
            'cover': 'green', 'started_on': '2026-05-10', 'finished_on': '2026-05-01',
        })
        self.assertContains(response, 'must be on or after the start date')

    def test_delete_book(self):
        response = self.client.post(reverse('library:book_delete', args=[self.book.pk]))
        self.assertRedirects(response, reverse('library:book_list'))
        self.assertFalse(Book.objects.exists())

    def test_author_pages(self):
        self.assertContains(self.client.get(reverse('library:author_list')), 'Mary Shelley')
        self.assertContains(self.client.get(self.author.get_absolute_url()), 'Frankenstein')
