from django.test import TestCase
from .models import Book
from django.urls import reverse
from users.models import CustomUser


class BookListTestcase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))
        # 'No books found.' list.html fayliga yozganmiz
        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="1234")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="12345")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="123456")

        response = self.client.get(reverse('books:list')+"?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse('books:list')+"?page=2&page_size=2")

        self.assertContains(response, book3)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="1234")

        response = self.client.get(reverse('books:book_detail', kwargs={"id":book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)


class BookReviewTesCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="1234")
        user = CustomUser.objects.create(
            username="user1", first_name='first1', last_name='last1', email='email@gmail.com'
        )
        user.set_password("12345")
        user.save()
        self.client.login(username='user1', password='12345')

        self.client.post(reverse("books:reviews", kwargs={"id":book.id}), data={
            "stars_given":3,
            "comment":"Nice book"
        })

        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)
