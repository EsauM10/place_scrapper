from typing import Any

class Place:
    def __init__(self, 
        title: str, 
        rating: float,
        recommendations: int,
        address: str,
        hours: dict[str, list[str]],
        phone: str,
        plus_code: str,
        image_url: str,
        url_to_maps: str
    ):
        self.title           = title
        self.rating          = rating
        self.recommendations = recommendations
        self.address         = address
        self.hours           = hours
        self.phone           = phone
        self.plus_code       = plus_code
        self.image_url       = image_url
        self.url_to_maps     = url_to_maps
    
    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            'title': self.title,
            'rating': self.rating,
            'recommendations': self.recommendations,
            'address': self.address,
            'hours': self.hours,
            'phone': self.phone,
            'plus_code': self.plus_code,
            'image_url': self.image_url,
            'url': self.url_to_maps
        }
    
    def __str__(self) -> str:
        return f'Place(title={self.title}, rating={self.rating}, address={self.address})'
    
