from place_scrapper.adapters import SeleniumScrapper
from place_scrapper.models import Place



class PlaceScrapper:
    @staticmethod
    def get_places(query: str) -> list[Place]:
        scrapper = SeleniumScrapper()
        urls = scrapper.get_place_urls(query)

        return scrapper.get_places(urls)
