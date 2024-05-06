from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
