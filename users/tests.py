from http import HTTPStatus
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse
from website_django import settings


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'username': 'user1',
            'firstname': 'Alexander',
            'email': 'user1@mail.ru',
            'password1': 'user1user1',
            'password2': 'user1user1'
        }

    def tearDown(self):
        pass

    def test_form_register_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_success(self):
        response = self.client.post(self.path, self.data)
        user_model = get_user_model()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_password_errors(self):
        self.data['password2'] += 'a'
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают.', html=True)

    def test_user_registration_uniq_username(self):
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_uniq_email(self):
        user_model = get_user_model()
        user_model.objects.create(email=self.data['email'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким E-mail уже зарегестрирован')
        self.assertTrue(user_model.objects.filter(email=self.data['email']).exists())


class LoginUserTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:login')
        self.data = {
            'username': 'user1',
            'email': 'user1@mail.ru',
            'password': 'user1user1'
        }
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'], email=self.data['email'])
        user = user_model.objects.get(username=self.data['username'])
        user.set_password(self.data['password'])
        user.save()

    def test_form_login_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_by_username_success(self):
        self.assertFalse(get_user(self.client).is_authenticated, "Пользователь уже активен")

        response = self.client.post(self.path, {'username': self.data['username'], 'password': self.data['password']})

        self.assertTrue(get_user(self.client).is_authenticated, "Пользователь не активен, вход не произведен")
        self.assertEqual(response.status_code, HTTPStatus.FOUND, "Переадресация не произошла")
        self.assertRedirects(response,
                             reverse(settings.LOGIN_REDIRECT_URL)), "Переодресация не на ожидаемую страницу"

    def test_user_login_by_email_success(self):
        self.assertFalse(get_user(self.client).is_authenticated, "Пользователь уже активен")

        response = self.client.post(self.path, {'username': self.data['email'], 'password': self.data['password']})

        self.assertTrue(get_user(self.client).is_authenticated, "Пользователь не активен, вход не произведен")
        self.assertEqual(response.status_code, HTTPStatus.FOUND, "Переадресация не произошла")
        self.assertRedirects(response,
                             reverse(settings.LOGIN_REDIRECT_URL)), "Переодресация не на ожидаемую страницу"


class ProfileUserTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:profile')
        self.data = {
            'username': 'user1',
            'email': 'user1@mail.ru',
            'password': 'user1user1',
            'first_name': 'Alexander'
        }
        self.user_model = get_user_model()
        self.user_model.objects.create_user(
            username=self.data['username'],
            password=self.data['password'],
            email=self.data['email'],
            first_name=self.data['first_name']
        )
        self.assertTrue(self.client.login(username=self.data['username'], password=self.data['password']))

    def test_form_user_profile_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html'), "Не тот шаблон html"

    def test_authenticated_user(self):
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_update_profile_success(self):
        data = {'first_name': 'Alexander1'}
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code,
                         HTTPStatus.FOUND), "После сохранения изменений не произошла переодресация"
        self.assertRedirects(response,
                             reverse('users:profile')), "Переодресация на другой адрес"
        self.assertEqual(
            data['first_name'],
            self.user_model.objects.get(username=self.data['username']).first_name
        ), "Изменения не сохранились в БД"

    def test_user_logout(self):
        response = self.client.post(reverse('users:logout'))
        self.assertFalse(get_user(self.client).is_authenticated), "Пользователь не вышел"
        self.assertEqual(response.status_code, HTTPStatus.FOUND), "Не выполнена переодресация после выхода"
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL)), "Переодресация на другой адрес"
