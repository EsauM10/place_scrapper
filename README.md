# Google Places Scrapper

## Instalation
```python
pip install git+https://github.com/EsauM10/place_scrapper.git
```

## Usage
```python
from place_scrapper import GooglePlaces

places = GooglePlaces.get_places(query='Restaurants in São Paulo')

for place in places:
    print(place)
```
