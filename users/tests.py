from http import HTTPStatus
from django.contrib.auth import get_user_model, get_user
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from selenium import webdriver

from tests.pages.login_page import LoginPage
from tests.pages.register_page import RegisterPage
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


class RegisterUserSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        # cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_register_form(self):
        page = RegisterPage(self.driver, f'{self.live_server_url}{reverse("users:register")}')
        page.open()
        page.should_be_register_form()

    def test_user_registration(self):
        page = RegisterPage(self.driver, f'{self.live_server_url}{reverse("users:register")}')
        page.open()
        user_model = get_user_model()
        data = {
            'username': 'user1',
            'firstname': 'Alexander',
            'email': 'user1@mail.ru',
            'password1': 'user1user1',
            'password2': 'user1user1'
        }
        page.input_data(*data.values())
        page.click_register_button()

        (self.assertEqual(
            self.driver.current_url,
            f'{self.live_server_url}{reverse("users:login")}'
        ), 'Не выполнена переадресация после регистрации пользователя')
        self.assertTrue(
            user_model.objects.filter(username='user1').exists()
        ), 'User не сохранился в БД после регистрации'


class LoginUserTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:login')
        self.data = {
            'username': 'user1',
            'password': 'user1user1'
        }
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        user = user_model.objects.get(username=self.data['username'])
        user.set_password(self.data['password'])
        user.save()

    def test_form_login_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_success(self):
        self.assertFalse(get_user(self.client).is_authenticated, "Пользователь уже активен")

        response = self.client.post(self.path, self.data)

        self.assertTrue(get_user(self.client).is_authenticated, "Пользователь не активен, вход не произведен")
        self.assertEqual(response.status_code, HTTPStatus.FOUND, "Переадресация не произошла")
        self.assertRedirects(response,
                             reverse(settings.LOGIN_REDIRECT_URL)), "Переодресация не на ожидаемую страницу"


class LoginUserSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        # cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_form(self):
        page = LoginPage(self.driver, f'{self.live_server_url}{reverse("users:login")}')
        page.open()
        page.should_be_login_form()

    def test_user_login_success(self):
        data = {
            'username': 'user1',
            'password': 'user1user',
        }
        user_model = get_user_model()
        user_model.objects.create(username=data['username'])
        user = user_model.objects.get(username=data['username'])
        user.set_password(data['password'])
        user.save()

        page = LoginPage(self.driver, f'{self.live_server_url}{reverse("users:login")}')
        page.open()
        page.input_data(username=data['username'], password=data['password'])
        page.click_login_button()

        self.assertEqual(
            self.driver.current_url,
            f'{self.live_server_url}{reverse(settings.LOGIN_REDIRECT_URL)}',
            'Не выполнена переадресация после авторизации пользователя'
        )

    def test_login_redirect(self):
        page = LoginPage(self.driver, f'{self.live_server_url}{reverse("users:login")}')
        page.open()
        page.click_registrate_redirect_button()
        self.assertTrue(
            self.driver.current_url, f'{self.live_server_url}{reverse("users:register")}'
        ), 'Не выполнен переход на страницу регистрации'
