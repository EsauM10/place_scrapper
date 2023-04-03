import pytest

from unittest.mock import patch

from place_scrapper.adapters.selenium.factories import PlaceFactory

from selenium.webdriver.remote.webelement import WebElement

def find_element_which_raises(selector: str):
    raise Exception()

def make_web_element() -> WebElement:
    class WebElementMock(WebElement):
        def __init__(self, parent, id_) -> None:
            super().__init__(parent, id_)
        
        def get_attribute(self, name: str) -> str:
            return name

        @property
        def text(self) -> str:
            return 'Some Text'
        
    return WebElementMock(id_=0, parent='')


def make_place_factory() -> PlaceFactory:
    class PlaceFactoryMock(PlaceFactory):
        def __init__(self, url: str, element: WebElement) -> None:
            super().__init__(url, element)
        
        def find_element_by_xpath(self, selector: str) -> WebElement:
            return self.element
        
    return PlaceFactoryMock(url='https://www.google.com/maps/place/', element=make_web_element())


# ============================================ Tests ============================================ #
def test_should_return_an_empty_title_when_get_title_raises(monkeypatch: pytest.MonkeyPatch):
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().title == ''
    

def test_should_return_a_place_with_correct_title():
    factory = make_place_factory()
    with patch('selenium.webdriver.remote.webelement.WebElement') as element:
        element.text = 'Place Title'
        factory.element = element
        assert factory.make_place().title == 'Place Title'


def test_should_return_a_rating_with_zero_value_when_get_rating_raises(monkeypatch: pytest.MonkeyPatch): 
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().rating == 0


def test_should_return_a_rating_with_correct_value(): 
    factory = make_place_factory()
    with patch('selenium.webdriver.remote.webelement.WebElement') as element:
        element.text = '4,5'
        factory.element = element
        assert factory.make_place().rating == 4.5


def test_should_return_a_recommendation_with_zero_value_when_get_rating_raises(monkeypatch: pytest.MonkeyPatch):
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().recommendations == 0


def test_should_return_a_recommendation_with_correct_value(): 
    factory = make_place_factory()
    with patch('selenium.webdriver.remote.webelement.WebElement') as element:
        element.text = '(1.444)'
        factory.element = element
        assert factory.make_place().recommendations == 1444


def test_should_return_an_empty_address_when_get_address_raises(monkeypatch: pytest.MonkeyPatch):
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().address == ''


def test_should_return_an_address_with_correct_value(monkeypatch: pytest.MonkeyPatch):
    def get_attribute(name: str):
        return 'Address: Alameda Campinas, 1630, São Paulo - SP, 01404-002 '

    factory = make_place_factory()
    monkeypatch.setattr(factory.element, 'get_attribute', get_attribute)
    assert factory.make_place().address == 'Alameda Campinas, 1630, São Paulo - SP, 01404-002'


def test_should_return_an_empty_phone_number_when_get_phone_raises(monkeypatch: pytest.MonkeyPatch):
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().phone == ''


def test_should_return_a_phone_number_with_correct_value(monkeypatch: pytest.MonkeyPatch):
    def get_attribute(name: str):
        return 'phone:tel:01155751900'
    
    factory = make_place_factory()
    monkeypatch.setattr(factory.element, 'get_attribute', get_attribute)
    assert factory.make_place().phone == '01155751900'


def test_should_return_an_empty_pluscode_when_get_plus_code_raises(monkeypatch: pytest.MonkeyPatch):
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().plus_code == ''


def test_should_return_a_pluscode_with_correct_value(monkeypatch: pytest.MonkeyPatch):
    def get_attribute(name: str):
        return 'Plus Code: C8GQ+MM Jardim Paulista, São Paulo - SP'
    
    factory = make_place_factory()
    monkeypatch.setattr(factory.element, 'get_attribute', get_attribute)
    assert factory.make_place().plus_code == 'C8GQ+MM Jardim Paulista, São Paulo - SP'


def test_should_return_an_empty_dict_when_get_business_hours_raises(monkeypatch: pytest.MonkeyPatch):
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().hours == {}


def test_should_return_a_dict_with_business_hours(monkeypatch: pytest.MonkeyPatch):
    def get_attribute(name: str):
        text = 'sábado, 12:00 a 15:00; domingo, 12:00 a 15:00; segunda-feira, 12:00 a 15:00; '
        text += 'terça-feira, 12:00 a 15:00; quarta-feira, 12:00 a 15:00; quinta-feira, 12:00 a 15:00; '
        text += 'sexta-feira, 12:00 a 15:00, Os horários podem ser diferentes. Ocultar horário de funcionamento da semana'
        return text
    
    factory = make_place_factory()
    monkeypatch.setattr(factory.element, 'get_attribute', get_attribute)
    assert factory.make_place().hours == {
        'sábado':        ['12:00 - 15:00'],
        'domingo':       ['12:00 - 15:00'],
        'segunda-feira': ['12:00 - 15:00'],
        'terça-feira':   ['12:00 - 15:00'],
        'quarta-feira':  ['12:00 - 15:00'],
        'quinta-feira':  ['12:00 - 15:00'],
        'sexta-feira':   ['12:00 - 15:00']
    }
    

def test_should_return_an_empty_url_when_get_image_url_raises(monkeypatch: pytest.MonkeyPatch):
    factory = make_place_factory()
    monkeypatch.setattr(factory, 'find_element_by_xpath', find_element_which_raises)
    assert factory.make_place().image_url == ''


def test_should_return_correct_image_url(monkeypatch: pytest.MonkeyPatch):
    def get_attribute(name: str):
        return 'https://www.google.com/maps/place/img.png'
    
    factory = make_place_factory()
    monkeypatch.setattr(factory.element, 'get_attribute', get_attribute)
    assert factory.make_place().image_url == get_attribute('src')


def test_should_ensure_the_place_url_is_the_same_which_was_passed():
    factory = make_place_factory()
    assert factory.make_place().url_to_maps == factory.url