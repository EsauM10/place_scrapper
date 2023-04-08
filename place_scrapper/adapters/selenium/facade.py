from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumDriver:
    def __init__(self, headless: bool = True) -> None:
        self.__driver = webdriver.Chrome(options=self.__make_options(headless))

    def __make_options(self, headless: bool) -> Options:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')

        if(headless):
            options.add_argument('--headless')
        return options
    
    def goto(self, url: str):
        self.__driver.get(url)

    def await_element(self, selector: str, timeout: float = 1) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, selector))
        )
    
    def find_element(self, selector: str) -> WebElement:
        return self.__driver.find_element(By.XPATH, value=selector)

    def scroll_element(self, scrollable_element: WebElement):
        self.__driver.execute_script(
            'arguments[0].scrollTo(0, arguments[0].scrollHeight)',
            scrollable_element
        )

    def close(self):
        self.__driver.close()