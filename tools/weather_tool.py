import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def clean_city_input(city):
    # Remove natural language noise
    city = city.replace("tomorrow", "").strip()
    return city


def get_weather(city):

    city = clean_city_input(city)

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": f"Weather API failed for {city}"}

    data = response.json()

    # Defensive validation
    if "main" not in data:
        return {"error": f"Invalid weather data for {city}"}

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }
