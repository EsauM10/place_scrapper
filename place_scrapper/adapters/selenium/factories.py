from place_scrapper.helpers import extract_numbers, parse_float, split_business_hours
from place_scrapper.models import Place
from place_scrapper.protocols import Selectors

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class PlaceFactory:
    def __init__(self, url: str, element: WebElement) -> None:
        self.url = url
        self.element = element
    
    def find_element_by_xpath(self, selector: str) -> WebElement:
        return self.element.find_element(By.XPATH, value=selector)

    def __get_address(self) -> str:
        try:
            aria_label = self.find_element_by_xpath(Selectors.PLACE_ADDRESS).get_attribute('aria-label')
            return aria_label.split(':').pop().strip()
        except:
            return ''

    def __get_business_hours(self) -> dict[str, list[str]]:
        try:
            aria_label = self.find_element_by_xpath(Selectors.PLACE_HOURS).get_attribute('aria-label')
            return split_business_hours(aria_label)
        except:
            return {}
    
    def __get_image_url(self) -> str:
        try:
            image = self.find_element_by_xpath(Selectors.PLACE_IMAGE)
            return image.get_attribute('src')
        except:
            return ''
    
    def __get_phone(self) -> str:
        try:
            button = self.find_element_by_xpath(Selectors.PLACE_PHONE)
            phone  = button.get_attribute('data-item-id')
            return extract_numbers(phone)[0]
        except:
            return ''
        
    def __get_plus_code(self) -> str:
        try:
            aria_label = self.find_element_by_xpath(Selectors.PLACE_PLUS_CODE).get_attribute('aria-label')
            return aria_label.split('Plus Code: ').pop()
        except:
            return ''

    def __get_rating(self) -> float:
        try:
            span = self.find_element_by_xpath(Selectors.PLACE_RATING)
            return parse_float(span.text)
        except:
            return 0
        
    def __get_recommendations(self) -> int:
        try: 
            span = self.find_element_by_xpath(Selectors.PLACE_RECOMMENDATIONS)
            recommendations = extract_numbers(span.text)[0]
            return int(recommendations.replace('.', ''))
        except:
            return 0
    
    def __get_title(self) -> str:
        try:
            return self.find_element_by_xpath(Selectors.PLACE_TITLE).text
        except:
            return ''

    def make_place(self) -> Place:
        return Place(
            title=self.__get_title(),
            rating=self.__get_rating(),
            recommendations=self.__get_recommendations(),
            address=self.__get_address(),
            hours=self.__get_business_hours(),
            phone=self.__get_phone(),
            plus_code=self.__get_plus_code(),
            image_url=self.__get_image_url(),
            url_to_maps=self.url
        )
    