from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from place_scrapper.adapters.selenium.factories import PlaceFactory
from place_scrapper.adapters.selenium.facade import SeleniumDriver
from place_scrapper.models import Place
from place_scrapper.protocols import Scrapper, Selectors


class SeleniumScrapper(Scrapper):
    def __init__(self) -> None:
        pass
    
    def get_articles_size(self, feed: WebElement) -> int:
        articles = feed.find_elements(By.XPATH, value=Selectors.ARTICLES)
        if(not articles): 
            raise Exception(f'Selectors.ARTICLES="{Selectors.ARTICLES}" not found')
        return len(articles)

    def scroll_until_end(self, driver: SeleniumDriver, feed: WebElement, limit: int):
        while self.get_articles_size(feed) < limit:
            try:
                driver.find_element(Selectors.FEED_FOOTER)
                break
            except:
                driver.scroll_element(feed)
    
    def get_place_urls(self, query: str, limit: int) -> list[str]:
        url = f'https://www.google.com/maps/search/{query}'
        driver = SeleniumDriver()

        try:
            driver.goto(url)
            feed = driver.await_element(Selectors.FEED, timeout=5)
            self.scroll_until_end(driver, feed, limit)
            articles = feed.find_elements(By.XPATH, value=Selectors.ARTICLES)

            return [
                article.find_element(By.XPATH, value='a').get_attribute('href')
                for article in articles[0:limit]
            ] # type: ignore
        except Exception as ex:
            print('[place_scrapper]:', ex) 
            return []
        finally:
            driver.close()
        

    def get_places(self, place_urls: list[str]) -> list[Place]:
        places = []
        driver = SeleniumDriver()
        
        try:
            for i, url in enumerate(place_urls):
                print(f'[place_scrapper]: Scrapping places... ({i+1}/{len(place_urls)})', end='\r')
                driver.goto(url)
                place_div = driver.await_element(Selectors.PLACE_CONTAINER, timeout=5)
                places.append(PlaceFactory(url, element=place_div).make_place())

        except: pass
        finally:
            driver.close()
        return places