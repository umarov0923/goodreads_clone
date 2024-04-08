from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.models import CustomUser
from books.models import Book, BookReview


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='admin', last_name='admin1')
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='admin', password='12345')

    def test_book_review_detail(self):
        book =Book.objects.create(title="Book1", description="Description1", isbn='123123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.get(reverse('api:review-detail', kwargs={'id':br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], "Book1")
        self.assertEqual(response.data['book']['description'], "Description1")
        self.assertEqual(response.data['book']['isbn'], "123123")
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['last_name'], "admin1")
        self.assertEqual(response.data['user']['username'], "admin")

    def test_delete_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='123123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
        response = self.client.delete(reverse('api:review-detail', kwargs={'id':br.id}) )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(book=book).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='123123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}), data={"stars_given":4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)

    def test_put_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='123123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
        data= {
            "stars_given":4,
            "comment":"nice book",
        }
        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}), data=data)
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book')

    def test_create_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn='123123')
        data = {
            "stars_given": 4,
            "comment": "nice book",
            "user_id":self.user.id,
            "book_id":book.id
        }

        response = self.client.post(reverse('api:review-list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book')

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='admin2', last_name='admin2')
        book = Book.objects.create(title="Book1", description="Description1", isbn='123123')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=5, comment="Very good book")

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        # self.assertEqual(response.data["results"][0]['id'], br_two.id)
        # self.assertEqual(response.data["results"][0]['stars_given'], br_two.stars_given)
        # self.assertEqual(response.data["results"][1]['id'], br.id)
        # self.assertEqual(response.data["results"][1]['stars_given'], br.stars_given)
