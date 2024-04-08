from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                "username": "admin1",
                "first_name": "Mukarramboy",
                "last_name": "Umarov",
                "email": "admin@gmail.com",
                "password": "12345"
            }
        )

        user = CustomUser.objects.get(username='admin1')

        self.assertEqual(user.first_name, 'Mukarramboy')
        self.assertEqual(user.last_name, 'Umarov')
        self.assertEqual(user.email, 'admin@gmail.com')
        self.assertNotEqual(user.password, '12345')

    def test_user_registration_missing_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "Mukarramboy",
                "email": "admin@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        # Проверяем, что пользователь не создан
        self.assertEqual(user_count, 0)

        # Проверяем, что ответ имеет статус код 200 (ОК)
        self.assertEqual(response.status_code, 200)


        # Предполагая, что вы используете встроенные в Django ошибки формы, проверяем наличие сообщений об ошибках в ответе
        self.assertContains(response, "This field is required.", count=2, status_code=200)

    # def test_invalid_email(self):
    #     response = self.client.post(
    #         reverse('users:register'),
    #         data={
    #             "username": "admin1",
    #             "first_name": "Mukarramboy",
    #             "last_name": "Umarov",
    #             "email": "admin-gmail.com",
    #             "password": "12345"
    #         }
    #     )
    # #
    #     user_count = CustomUser.objects.count()
    #     self.assertEqual(user_count, 0)
    #     self.assertFormError(response, "form", "email", "Enter a valid email address.")
    #
    # def test_unique_username(self):
    #     user = CustomUser.objects.create(username='admin1', first_name='Mukarramboy')
    #     user.set_password('12345')
    #     user.save()
    #
    #     response =  self.client.post(
    #         reverse('users:register'),
    #         data={
    #             "username": "admin1",
    #             "first_name": "Mukarramboy1",
    #             "last_name": "Umarov1",
    #             "email": "admin@gmail1.com",
    #             "password": "12345"
    #         }
    #     )
    #
    #     user_count = CustomUser.objects.count()
    #     self.assertEqual(user_count, 1)
    #     self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='admin', last_name='admin1')
        self.db_user.set_password('12345')
        self.db_user.save()

    def test_successful_login(self):

        self.client.post(
            reverse('users:login'),
            data={
                "username": 'admin',
                "password": "12345"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": 'admin1',
                "password": "12345"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                "username": 'admin1',
                "password": "notogri parol"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="user1", password='12345')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/user/profile/')

    def test_profile_details(self):
        user = CustomUser.objects.create(username="user1", first_name='first1', last_name='last1', email='email@gmail.com')
        user.set_password('12345')
        user.save()

        self.client.login(username="user1", password='12345')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)

    def test_update_profile(self):
        user = CustomUser.objects.create(username="user1", first_name='first1', last_name='last1', email='email@gmail.com')
        user.set_password('12345')
        user.save()
        self.client.login(username="user1", password='12345')

        response = self.client.post(
            reverse("users:profile_edit"),
            data={
                "username":"user1",
                "first_name":"first1",
                "last_name":"Doe",
                "email":"email2@gmail.com"
            }
        )
        # CustomUser = CustomUser.objects.get(id=CustomUser.id)
        # Eng yaxshi yol -->
        user.refresh_from_db()

        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'email2@gmail.com')
        self.assertEqual(response.url, reverse("users:profile"))

