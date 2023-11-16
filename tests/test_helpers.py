import time
import pytest
from pytest import MonkeyPatch

from place_scrapper import helpers

def test_should_extract_hours_from_a_string():
    values = {
        '12:00:15 to 15:00, 19:00 to 23:00': ['12:00', '15:00', '19:00', '23:00'],
        '12:00abc15:000': ['12:00', '15:00'],
        '09:a0 10:0O 11:00': ['11:00'],
        'abcdef14:00ghijklm': ['14:00'],
        'Some Text': [],
        '1200 - 1500': [],
    }
    for value, expected in values.items():
        result = helpers.extract_hours(value)
        assert result == expected


def test_should_extract_numbers_from_a_string():
    values = {
        '12:00:15 to 15,3,14': ['12', '00', '15', '15,3', '14'],
        '12.00 - (1.500)': ['12.00', '1.500'],
        '12abc15,000': ['12', '15,000'],
        'abcdefghijklm': [],
        'PI is 3,14, Eulers Constant is 0.57': ['3,14', '0.57'],
        'Some:1800Text': ['1800'],
        '1.000.000 years': ['1.000', '000']   
    }
    for value, expected in values.items():
        result = helpers.extract_numbers(value)
        assert result == expected


def test_should_return_true_if_string_is_a_positive_number():
    values = {
        '1200,45': True,
        '1.500': True,
        '1.455.555': False,
        '(1.500)': False,
        '15-000': False,
        'abcdefghijklm': False,
        '-3,14': False,
        '1800y': False,
        '3,1415': True
    }
    for value, expected in values.items():
        result = helpers.string_is_a_number(value)
        assert result == expected


def test_should_return_a_formatted_hours_list():
    values = [
        '17:00 to 18:00', '15:00to18:00', '12:0 to 14:00', 
        'Some Text',
        '19:00, 20:00, 21:00',
        '8 AM to 12 PM'
    ]
    assert helpers.join_hours(values) == [
        '17:00 - 18:00',
        '15:00 - 18:00',
        '14:00',
        '19:00 - 20:00 - 21:00'
    ]


def test_should_return_a_dict_with_business_hours():
    text =  'saturday, 12:00 a 15:00, 19:00 a 23:00; sunday, Closed; '
    text += 'monday, 12:00 a 15:00, 17:00 a 23:00; tuesday, 12:00 a 15:00, 19:00 a 23:00; ' 
    text += 'wednesday, 19:00 a 23:00; thursday, 08:00 a 12:00, 13:00 a 17:00, 19:00 a 23:00; '
    text += 'friday, 12:00 a 15:00, 19:00 a 23:00, Hours might differ. Hide open hours for the week.'
    
    assert helpers.split_business_hours(text) == {
        'saturday':  ['12:00 - 15:00', '19:00 - 23:00'],
        'sunday':    [],
        'monday':    ['12:00 - 15:00', '17:00 - 23:00'],
        'tuesday':   ['12:00 - 15:00', '19:00 - 23:00'],
        'wednesday': ['19:00 - 23:00'],
        'thursday':  ['08:00 - 12:00', '13:00 - 17:00', '19:00 - 23:00'],
        'friday':    ['12:00 - 15:00', '19:00 - 23:00']
    }


def test_should_return_an_empty_dict_when_incorrect_data_is_provided():
    text = 'Hours might differ. Hide open hours for the week.'
    assert helpers.split_business_hours(text) == {}


def test_should_parse_a_string_to_a_float_value():
    default_value = -1
    values = {
        '(4.5)': default_value,
        '1000': 1000,
        '003.14': 3.14,
        '0.055': 0.055,
        '-2': default_value,
        '1,80': 1.8,
        'Some Text 123': default_value,
    }
    
    for value, expected in values.items():
        result = helpers.parse_float(value, default=default_value)
        assert result == expected


def test_should_return_true_if_timeout_expired(monkeypatch: MonkeyPatch):
    initial_time = time.time()
    timeout = 10
    add_ten_seconds = lambda: initial_time + timeout + 1
    monkeypatch.setattr(time, 'time', add_ten_seconds)
    assert helpers.is_timed_out(initial_time, timeout) == True


def test_should_return_false_if_timeout_not_expired(monkeypatch: MonkeyPatch):
    initial_time = time.time()
    timeout = 10
    add_ten_seconds = lambda: initial_time + timeout
    monkeypatch.setattr(time, 'time', add_ten_seconds)
    assert helpers.is_timed_out(initial_time, timeout) == False


def test_should_raise_a_exception_when_incorrect_urls_are_provided():
    urls = [
        'Man%C3%AD/data=!4m7!3m6!1s0x94ce575aaccf6f9f',
        'Man%C3%AD',
        ''
    ]
    with pytest.raises(ValueError):
        for url in urls:
            helpers.get_title_from_url(url)


def test_should_return_the_place_name_when_correct_urls_are_provided():
    urls = {
        'https://www.google.com/maps/place/Man%C3%AD/data=!4m7!3m6!1s0x94ce575aaccf6f9f': 'Maní',
        'https://www.google.com/maps/place/Chef+Rouge/data=!4m7!3m6!1s0x94ce58346f0fe53f': 'Chef Rouge',
        'https://www.google.com/maps/place/Restaurante+Mesti%C3%A7o/data=!4m7!3m6!1s0x94ce583236457555': 'Restaurante Mestiço',
        'https://www.google.com/maps/place/Pettirosso+Ristorante/data=!4m7!3m6!1s0x94ce582aa63facf5': 'Pettirosso Ristorante',
        'https://www.google.com/maps/place/Seen+-+Restaurant+%26+Bar/data=!4m7!3m6!1s0x94ce59c8b': 'Seen - Restaurant & Bar',
        'https://www.google.com/maps/place/Pi%C3%B9+Pinheiros/data=!4m7!3m6!1s0x94ce57bacc6ef64d': 'Più Pinheiros',
        'https://www.google.com/maps/place/A+Figueira+Rubaiyat/data=!4m7!3m6!1s0x94ce583397637bdb': 'A Figueira Rubaiyat',
        'https://www.google.com/maps/place/Roi+M%C3%A9diterran%C3%A9e/data=!4m7!3m6!1s0x94ce593f94bbfd4b': 'Roi Méditerranée'
    }
    for url, title in urls.items():
        assert helpers.get_title_from_url(url) == title