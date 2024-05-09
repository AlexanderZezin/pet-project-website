from selenium.common import NoSuchElementException
from selenium import webdriver


class BasePage:
    def __init__(self, driver, url):
        self.driver: webdriver.Chrome = driver
        self.url: str = url

    def open(self):
        self.driver.get(self.url)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(how, what)
        except NoSuchElementException:
            return False
        return True
