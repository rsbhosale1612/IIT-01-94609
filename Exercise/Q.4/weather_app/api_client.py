import requests
from .config import API_KEY, UNITS

BASE_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"  

class WeatherAPIError(Exception):
    pass

def get_current_weather(city: str, timeout=10):
    params = {"q": city, "appid": API_KEY, "units": UNITS}
    try:
        resp = requests.get(BASE_CURRENT, params=params, timeout=timeout)
        if resp.status_code != 200:
          
            data = resp.json()
            raise WeatherAPIError(f"{resp.status_code}: {data.get('message', 'API error')}")
        return resp.json()
    except requests.RequestException as e:
        raise WeatherAPIError(f"Network error: {e}") from e

def get_forecast(city: str, timeout=10):
    params = {"q": city, "appid": API_KEY, "units": UNITS}
    try:
        resp = requests.get(BASE_FORECAST, params=params, timeout=timeout)
        if resp.status_code != 200:
            data = resp.json()
            raise WeatherAPIError(f"{resp.status_code}: {data.get('message', 'API error')}")
        return resp.json()
    except requests.RequestException as e:
        raise WeatherAPIError(f"Network error: {e}") from e
