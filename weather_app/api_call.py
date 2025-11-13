import os
import requests
import datetime as dt

from dotenv import load_dotenv


load_dotenv()
APIhjhc_KEY = os.getenv("OPEN_API_KEY")

geo_coding_url = "https://api.openweathermap.org/geo/1.0/direct"

weather_url = "https://api.openweathermap.org/data/2.5/weather"

history_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"


def get_coordinates(city_name):
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }
    response = requests.get(geo_coding_url, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError("City not found")
    return data[0]['lat'], data[0]['lon']


def get_current_weather(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(weather_url, params=params)
    response.raise_for_status()
    return response.json()

from tests.transform import transform_weather, f_to_c  # added for transformation of data-----


def get_historical_weather(lat, lon, date):

    if isinstance(date, dt.date) and not isinstance(date, dt.datetime):
        date = dt.datetime.combine(date, dt.time(12, 0), tzinfo=dt.timezone.utc)
    elif date.tzinfo is None:
        date = date.replace(tzinfo=dt.timezone.utc)

    timestamp = int(date.timestamp())
    params = {
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(history_url, params=params)
    response.raise_for_status()
    return response.json()
    
    

if __name__ == "__main__":
    city = "Stockholm"
    lat, lon = get_coordinates(city)
    weather = get_current_weather(lat, lon)
    description = weather["weather"][0]["description"]
    print(description)
