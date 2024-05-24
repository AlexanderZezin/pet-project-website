from .base_page import BasePage
from .locators import PasswordChangePageLocators as PCPL


class PasswordChangePage(BasePage):
    def should_by_password_change_from(self):
        assert self.is_element_present(*PCPL.PASSWORD_CHANGE_FORM), 'Не найдена форма смены пароля'
        assert self.is_element_present(*PCPL.OLD_PASSWORD_INPUT), 'Не найдено поле ввода старого пароля'
        assert self.is_element_present(*PCPL.NEW_PASSWORD1_INPUT), 'Не найдено поле ввода нового пароля1'
        assert self.is_element_present(*PCPL.NEW_PASSWORD2_INPUT), 'Не найдено поле ввода нового пароля2'
        assert self.is_element_present(*PCPL.CHANGE_PASSWORD_BUTTON), 'Не найдена кнопка изменения пароля'

    def input_data(self, old_password, new_password1, new_password2):
        self.driver.find_element(*PCPL.OLD_PASSWORD_INPUT).send_keys(old_password)
        self.driver.find_element(*PCPL.NEW_PASSWORD1_INPUT).send_keys(new_password1)
        self.driver.find_element(*PCPL.NEW_PASSWORD2_INPUT).send_keys(new_password2)

    def click_password_change_button(self):
        self.driver.find_element(*PCPL.CHANGE_PASSWORD_BUTTON).click()
