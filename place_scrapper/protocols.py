from abc import ABC, abstractmethod

from place_scrapper.models import Place


class Selectors:
    ARTICLES: str               = '//div[@class="Nv2PK THOPZb CpccDe "]'
    FEED: str                   = '//div[@role="feed"]'
    FEED_FOOTER: str            = '//div[@class="m6QErb tLjsW eKbjU"]'
    PLACE_ADDRESS: str          = '//img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/place_gm_blue_24dp.png"]/../../../..'
    PLACE_CONTAINER: str        = '//div[@role="main"]'
    PLACE_HOURS: str            = '//img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/schedule_gm_blue_24dp.png"]/../../div[2]'
    PLACE_IMAGE: str            = '//div[@class="RZ66Rb FgCUCc"]/button/img'
    PLACE_RATING: str           = '//div[@class="F7nice "]/span[1]/span[1]'
    PLACE_RECOMMENDATIONS: str  = '//div[@class="F7nice "]/span[2]/span[1]'
    PLACE_TITLE: str            = '//h1[@class="DUwDvf lfPIob"]'
    PLACE_PHONE: str            = '//img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/phone_gm_blue_24dp.png"]/../../../..'
    PLACE_PLUS_CODE: str        = '//img[@src="//maps.gstatic.com/mapfiles/maps_lite/images/2x/ic_plus_code.png"]/../../../..'
    


class Scrapper(ABC):
    @abstractmethod
    def get_places(self, place_urls: list[str]) -> list[Place]:
        pass

    @abstractmethod
    def get_place_urls(self, query: str, limit: int) -> list[str]:
        pass

