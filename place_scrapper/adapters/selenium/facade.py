import undetected_chromedriver as chromedriver

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumDriver:
    def __init__(self, headless: bool = True) -> None:
        self.__driver = chromedriver.Chrome(headless=headless)

    def goto(self, url: str):
        self.__driver.get(url)

    def await_element(self, selector: str, timeout: float = 1) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, selector))
        )
    
    def find_element(self, selector: str) -> WebElement:
        return self.__driver.find_element(By.XPATH, value=selector)

    def scroll_until_find(self, scrollable_element: WebElement, selector: str):
        while True:
            try:
                self.find_element(selector)
                break
            except:
                scrollable_element.send_keys(Keys.PAGE_DOWN)

    def close(self):
        self.__driver.close()