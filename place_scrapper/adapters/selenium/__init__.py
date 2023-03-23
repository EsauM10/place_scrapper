from selenium.webdriver.common.by import By

from place_scrapper.adapters.selenium.factories import PlaceFactory
from place_scrapper.adapters.selenium.facade import SeleniumDriver
from place_scrapper.models import Place
from place_scrapper.protocols import Scrapper, Selectors


class SeleniumScrapper(Scrapper):
    def __init__(self) -> None:
        pass
    

    def get_place_urls(self, query: str) -> list[str]:
        url = f'https://www.google.com/maps/search/{query}'
        driver = SeleniumDriver()

        try:
            driver.goto(url)
            feed = driver.await_element(Selectors.FEED, timeout=5)
            driver.scroll_until_find(feed, Selectors.FEED_FOOTER)
            articles = feed.find_elements(By.XPATH, value=Selectors.ARTICLES)

            return [
                article.find_element(By.XPATH, value='a').get_attribute('href')
                for article in articles
            ]
        except: 
            return []
        finally:
            driver.close()
        

    def get_places(self, place_urls: list[str]) -> list[Place]:
        places = []
        driver = SeleniumDriver()

        try:
            for url in place_urls:
                driver.goto(url)
                place_div = driver.await_element(Selectors.PLACE_CONTAINER, timeout=5)
                places.append(PlaceFactory(url, element=place_div).make_place())
        except: pass
        finally:
            driver.close()
        return places