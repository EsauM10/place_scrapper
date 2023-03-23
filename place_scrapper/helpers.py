import re

HOUR_FORMAT = r'\d{2}:\d{2}'
POSITIVE_NUMBER = r'\d+(?:\,|\.)?\d+'

def extract_hours(value: str) -> list[str]:
    return re.findall(pattern=HOUR_FORMAT, string=value)

def extract_numbers(value: str) -> list[str]:
    return re.findall(pattern=POSITIVE_NUMBER, string=value)

def string_is_a_number(value: str) -> bool:
    if(re.match(pattern=f'^{POSITIVE_NUMBER}$', string=value)): 
        return True
    return False

def split_business_hours(hours: str) -> dict[str, str]:
    business_hours = {}
    for item in hours.split(';'):
        data = item.split(',')
        weekday = data[0].strip()
        hour = extract_hours(data[1])
        business_hours.update({weekday: ' - '.join(hour)})
    return business_hours

def parse_float(value: str, default: float = 0) -> float:
    if(string_is_a_number(value)):
        return float(value.replace(',', '.'))
    return default

