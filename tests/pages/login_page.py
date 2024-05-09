from .base_page import BasePage
from .locators import LoginPageLocators as LPL


class LoginPage(BasePage):
    def should_be_login_form(self):
        assert self.is_element_present(*LPL.LOGIN_FORM), "Не найдена форма авторизации"
        assert self.is_element_present(*LPL.USERNAME_INPUT), "Не найдено поле ввода username"
        assert self.is_element_present(*LPL.PASSWORD_INPUT), "Не найдено поле ввода password"
        assert self.is_element_present(*LPL.LOGIN_BUTTON), "Не найдена кнопка авторизации"
        assert self.is_element_present(
            *LPL.REGISTRATE_REDIRECT_BUTTON), "Не найдена кнопка перехода на страницу регистрации"

    def input_data(self, username, password):
        self.driver.find_element(*LPL.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*LPL.PASSWORD_INPUT).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*LPL.LOGIN_BUTTON).click()

    def click_registrate_redirect_button(self):
        self.driver.find_element(*LPL.REGISTRATE_REDIRECT_BUTTON).click()
