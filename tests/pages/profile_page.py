from .base_page import BasePage
from .locators import ProfilePageLocators as PPL


class ProfilePage(BasePage):
    def should_by_profile_form(self):
        assert self.is_element_present(*PPL.PROFILE_FORM), "Не найдена форма пользователя"
        assert self.is_element_present(*PPL.FIRST_NAME_INPUT), "Не найдено поле ввода имени пользователя"
        assert self.is_element_present(*PPL.LAST_NAME_INPUT), "Не найдено поле ввода фамилии пользователя"
        assert self.is_element_present(*PPL.UPDATE_BUTTON), "Не найдена кнопка сохранения изменений"
        assert self.is_element_present(*PPL.CHANGE_PASSWORD_LINK), "Не найдена ссылка на изменение пароля"

    def should_by_logout_button(self):
        assert self.is_element_present(*PPL.LOGOUT_BUTTON), "Не найдена кнопка выхода из профиля"

    def get_current_first_name(self):
        return self.driver.find_element(*PPL.FIRST_NAME_INPUT).get_attribute('value')

    def get_current_last_name(self):
        return self.driver.find_element(*PPL.LAST_NAME_INPUT).get_attribute('value')

    def change_first_name(self, first_name):
        self.driver.find_element(*PPL.FIRST_NAME_INPUT).clear()
        self.driver.find_element(*PPL.FIRST_NAME_INPUT).send_keys(first_name)

    def change_last_name(self, last_name):
        self.driver.find_element(*PPL.LAST_NAME_INPUT).clear()
        self.driver.find_element(*PPL.LAST_NAME_INPUT).send_keys(last_name)

    def click_update_button(self):
        self.driver.find_element(*PPL.UPDATE_BUTTON).click()

    def click_logout_button(self):
        self.driver.find_element(*PPL.LOGOUT_BUTTON).click()

    def click_change_password_button(self):
        self.driver.find_element(*PPL.CHANGE_PASSWORD_LINK).click()
