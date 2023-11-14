from setuptools import setup, find_packages

setup(
    name="place_scrapper",
    version="0.1.5",
    description='Scrapping package to retrieve data from Google Places.',
    long_description='Scrapping package to retrieve data from Google Places.',
    keywords=['google places', 'maps', 'scrapping', 'selenium'],
    url='https://github.com/EsauM10/place_scrapper',
    author='Esaú Mascarenhas',
    install_requires = [
        'selenium'
    ],
    packages=find_packages(),
    zip_safe=False
)