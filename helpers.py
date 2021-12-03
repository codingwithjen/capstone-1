"""Implements various helpers."""

import requests
API_SECRET_KEY = "s"

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="

def kelvin_to_F(K):
    return int((K - 273.15) * 9/5 + 32)

def kelvin_to_C(K):
    return int(K - 273.15)

def get_results(city):
    res = requests.get(f"{API_BASE_URL}/city", params={'city': city, 'key': API_SECRET_KEY})
    data = res.json()
    weather_results = {
        'city': res['name'].title(),
        'country': res['sys']['country'].upper(),
        'fahrenheit': kelvin_to_F(res['temp']['feels_like']),
    }
    return weather_results
