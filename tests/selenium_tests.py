from django.contrib.auth import get_user_model, authenticate, get_user
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from tests.pages.login_page import LoginPage
from tests.pages.profile_page import ProfilePage
from tests.pages.register_page import RegisterPage
from website_django import settings


class RegisterUserSeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.page = RegisterPage(self.driver, f'{self.live_server_url}{reverse("users:register")}')
        self.page.open()

    def tearDown(self):
        self.driver.quit()

    def test_register_form(self):
        self.page.should_be_register_form()

    def test_user_registration(self):
        user_model = get_user_model()
        data = {
            'username': 'user1',
            'firstname': 'Alexander',
            'email': 'user1@mail.ru',
            'password1': 'user1user1',
            'password2': 'user1user1'
        }
        self.page.input_data(*data.values())
        self.page.click_register_button()

        (self.assertEqual(
            self.driver.current_url,
            f'{self.live_server_url}{reverse("users:login")}'
        ), 'Не выполнена переадресация после регистрации пользователя')
        self.assertTrue(
            user_model.objects.filter(username='user1').exists()
        ), 'User не сохранился в БД после регистрации'

    def test_login_link_button(self):
        self.page.click_login_link_button()
        self.assertEqual(
            self.driver.current_url,
            f'{self.live_server_url}{reverse("users:login")}',
            "Не выполнен переход на страницу авторизации"
        )


class LoginUserSeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.data = {
            'username': 'user1',
            'email': 'user1@mail.ru',
            'password': 'user1user1',
        }
        user_model = get_user_model()
        user_model.objects.create_user(username=self.data['username'], email=self.data['email'])
        user = user_model.objects.get(username=self.data['username'])
        user.set_password(self.data['password'])
        user.save()

        self.driver = webdriver.Chrome()
        self.page = LoginPage(self.driver, f'{self.live_server_url}{reverse("users:login")}')
        self.page.open()

    def tearDown(self):
        self.driver.quit()

    def test_login_form(self):
        self.page.should_be_login_form()

    def test_user_login_by_username_success(self):
        self.page.input_data(username=self.data['username'], password=self.data['password'])
        self.page.click_login_button()

        self.assertEqual(
            self.driver.current_url,
            f'{self.live_server_url}{reverse(settings.LOGIN_REDIRECT_URL)}',
            'Не выполнена переадресация после авторизации пользователя'
        )

    def test_user_login_by_email_success(self):
        self.page.input_data(username=self.data['email'], password=self.data['password'])
        self.page.click_login_button()

        self.assertEqual(
            self.driver.current_url,
            f'{self.live_server_url}{reverse(settings.LOGIN_REDIRECT_URL)}',
            'Не выполнена переадресация после авторизации пользователя'
        )

    def test_registrate_link_button(self):
        self.page.click_registrate_redirect_button()
        self.assertTrue(
            self.driver.current_url, f'{self.live_server_url}{reverse("users:register")}'
        ), 'Не выполнен переход на страницу регистрации'


class ProfileUserSeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.data = {
            'username': 'user1',
            'first_name': 'Myname',
            'email': 'user1@mail.ru',
            'password': 'user1user1',
        }
        self.new_data = {
            'first_name': 'Mynewname'
        }
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username=self.data['username'],
            email=self.data['email'],
            first_name=self.data['first_name'],
            password=self.data['password']
        )

        self.driver = webdriver.Chrome()
        self.assertTrue(self.client.login(username=self.data['username'], password=self.data['password']))
        self.assertTrue(get_user(self.client).is_authenticated)
        self.driver.get(f'{self.live_server_url}/users/login')
        self.page = ProfilePage(self.driver, f'{self.live_server_url}{reverse("users:profile")}')
        self.page.open()

    def tearDown(self):
        self.driver.quit()

    def test_open_page(self):
        self.driver.implicitly_wait(2)
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}{reverse("users:profile")}')

    # def test_profile_form(self):
    #     self.page.should_by_profile_form()

    # def test_update_profile(self):
    #     old_name = self.page.get_current_first_name()
    #     self.page.change_first_name(self.new_data['first_name'])
    #     self.page.click_update_button()
    #
    #     self.assertEqual(old_name, self.page.get_current_first_name())
