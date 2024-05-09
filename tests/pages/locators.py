from selenium.webdriver.common.by import By


class RegistrationPageLocators:
    REGISTER_FORM = (By.CSS_SELECTOR, '[name=register_form]')
    USERNAME_INPUT = (By.NAME, "username")
    FIRST_NAME_INPUT = (By.NAME, 'first_name')
    EMAIL_INPUT = (By.NAME, 'email')
    PASSWORD1_INPUT = (By.NAME, 'password1')
    PASSWORD2_INPUT = (By.NAME, 'password2')
    REGISTRATE_BUTTON = (By.CSS_SELECTOR, 'form button:first-child')
    LOGIN_REDIRECT_BUTTON = (By.CSS_SELECTOR, 'form button:last-child')


class LoginPageLocators:
    LOGIN_FORM = (By.CSS_SELECTOR, '[name=login_form]')
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'form button:first-child')
    REGISTRATE_REDIRECT_BUTTON = (By.CSS_SELECTOR, 'form button:last-child')
