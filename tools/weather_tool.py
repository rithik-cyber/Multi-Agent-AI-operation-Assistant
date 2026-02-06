import os
import requests
from dotenv import load_dotenv
from llm.logger import logger

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    logger.info(f"Fetching weather for: {city}")

    url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }

        return weather_info

    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return {"error": str(e)}
