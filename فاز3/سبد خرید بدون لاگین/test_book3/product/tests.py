from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Book, Category


# Create your tests here.
class CategoryTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            full_name='zahra',
            email='zahra.kh2005@email.com',
            password='123456'
        )

        self.category = Category.objects.create(
            name='Art',
            user=self.user,
            slug='catt'
        )

    def test_category_listing(self):
        self.assertEqual(f'{self.category.name}', 'Art')

    def test_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), '/catt/')


class BookTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            full_name='zahra',
            email='zahra.kh2005@email.com',
            password='123456'
        )

        self.book = Book.objects.create(
            name='python',
            author='django',
            price='700',
            user=self.user,
            slug='boook'
        )

    #
    def test_book_listing(self):
        self.assertEqual(f'{self.book.name}', 'python')
        self.assertEqual(f'{self.book.author}', 'django')
        self.assertEqual(f'{self.book.price}', '700')

    def test_get_absolute_url(self):
        self.assertEqual(self.book.get_absolute_url(), '/1/boook/')
