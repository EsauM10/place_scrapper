![](https://img.shields.io/badge/python-3.9+-blue.svg)
![](https://img.shields.io/badge/selenium-4.8+-silver.svg)
![Tests](https://github.com/EsauM10/place_scrapper/actions/workflows/tests.yml/badge.svg)
# Google Places Scrapper

## Installation
```
pip install git+https://github.com/EsauM10/place_scrapper.git
```

## Usage
```python
from place_scrapper import GooglePlaces

places = GooglePlaces.get_places(query='Restaurants in São Paulo', limit=10)

for place in places:
    print(place)
```
### Saving to a file:
```python
import json
from place_scrapper import GooglePlaces

places = GooglePlaces.get_places(query='Restaurants in São Paulo')
data = [place.to_dict for place in places]
    
with open('places.json', mode='w', encoding='utf-8') as file:
    file.write(json.dumps(data))
```

