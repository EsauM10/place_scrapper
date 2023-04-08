from place_scrapper.adapters import SeleniumScrapper
from place_scrapper.models import Place



class GooglePlaces:
    @staticmethod
    def get_places(query: str, limit: int = 120) -> list[Place]:
        scrapper = SeleniumScrapper()
        urls = scrapper.get_place_urls(query, limit)

        return scrapper.get_places(urls)
