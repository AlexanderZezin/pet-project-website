from .base_page import BasePage
from .locators import RegistrationPageLocators as RPL


class RegisterPage(BasePage):
    def should_be_register_form(self):
        assert self.is_element_present(*RPL.REGISTER_FORM), "Не найдена форма регистрации"
        assert self.is_element_present(*RPL.USERNAME_INPUT), "Не найдено поле ввода username"
        assert self.is_element_present(*RPL.FIRST_NAME_INPUT), "Не найдено поле ввода first_name"
        assert self.is_element_present(*RPL.EMAIL_INPUT), "Не найдено поле ввода email"
        assert self.is_element_present(*RPL.PASSWORD1_INPUT), "Не найдено поле ввода password1"
        assert self.is_element_present(*RPL.PASSWORD2_INPUT), "Не найдено поле ввода password2"
        assert self.is_element_present(*RPL.REGISTRATE_BUTTON), "Не найдена кнопка регистрации"
        assert self.is_element_present(*RPL.LOGIN_REDIRECT_BUTTON), "Не найдена кнопка перехода на страницу авторизации"

    def click_register_button(self):
        self.driver.find_element(*RPL.REGISTRATE_BUTTON).click()

    def input_data(self, username, first_name, email, password1, password2):
        self.driver.find_element(*RPL.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*RPL.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*RPL.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*RPL.PASSWORD1_INPUT).send_keys(password1)
        self.driver.find_element(*RPL.PASSWORD2_INPUT).send_keys(password2)
