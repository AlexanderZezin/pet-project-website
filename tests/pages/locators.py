from selenium.webdriver.common.by import By


class RegistrationPageLocators:
    REGISTER_FORM = (By.NAME, 'register_form')
    USERNAME_INPUT = (By.NAME, "username")
    FIRST_NAME_INPUT = (By.NAME, 'first_name')
    EMAIL_INPUT = (By.NAME, 'email')
    PASSWORD1_INPUT = (By.NAME, 'password1')
    PASSWORD2_INPUT = (By.NAME, 'password2')
    REGISTRATE_BUTTON = (By.CSS_SELECTOR, 'form button:first-child')
    LOGIN_LINK_BUTTON = (By.CSS_SELECTOR, 'form button:last-child')


class LoginPageLocators:
    LOGIN_FORM = (By.NAME, 'login_form')
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'form button:first-child')
    REGISTRATE_LINK_BUTTON = (By.CSS_SELECTOR, 'form button:last-child')


class ProfilePageLocators:
    PROFILE_FORM = (By.NAME, 'profile_form')
    FIRST_NAME_INPUT = (By.NAME, "first_name")
    LAST_NAME_INPUT = (By.NAME, "last_name")
    UPDATE_BUTTON = (By.CSS_SELECTOR, 'form[name=profile_form] button')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, 'form[name=logout_form] button')
    CHANGE_PASSWORD_LINK = (By.XPATH, '//body/a')


class PasswordChangePageLocators:
    PASSWORD_CHANGE_FORM = (By.NAME, 'password_change_form')
    OLD_PASSWORD_INPUT = (By.NAME, 'old_password')
    NEW_PASSWORD1_INPUT = (By.NAME, 'new_password1')
    NEW_PASSWORD2_INPUT = (By.NAME, 'new_password2')
    CHANGE_PASSWORD_BUTTON = (By.CSS_SELECTOR, 'form[name=password_change_form] button')
