"""Implements various helpers."""

# import os, json, requests
# from datetime import datetime
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.environ.get('API_SECRET_KEY')
# API_BASE_URL = "https://api.openweathermap.org/"



# def get_weather_data(city):
#     url = f'{API_BASE_URL}/data/2.5/weather?q={city}&appid={API_KEY}'
#     res = requests.get(url).json()
#     return res

# def kelvin_to_F(K):
#     return int((K - 273.15) * 9/5 + 32)

# def kelvin_to_C(K):
#     return int(K - 273.15)


    # res = requests.get(f"{API_BASE_URL}/data/2.5/weather?q={city}&appid={API_KEY}")
    # data = res.json()
    # weather_results = {
    #     'city': res['name'].title(),
    #     'country': res['sys']['country'].upper(),
    #     'weather': res['weather'][0]['main'],
    #     'fahrenheit': '{0:2f}'.format(res['temp']['feels_like']),
    # }

    # return weather_results

# def get_weather_data(city):
#     res = requests.get(f"{API_BASE_URL}/city", params={'city': city, 'key': API_SECRET_KEY})
#     data = res.json()
#     weather_results = {
#         'city': res['name'].title(),
#         'country': res['sys']['country'].upper(),
#         'fahrenheit': kelvin_to_F(res['temp']['feels_like']),
#     }
#     return weather_results

