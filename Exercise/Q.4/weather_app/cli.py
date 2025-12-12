from .api_client import get_current_weather, get_forecast, WeatherAPIError
from .formatter import format_current, format_simple_forecast

def run_cli():
    print("Simple Weather CLI — enter city (or 'quit')")
    while True:
        city = input("City: ").strip()
        if not city or city.lower() in ("quit", "q", "exit"):
            print("Goodbye.")
            break
        try:
            current = get_current_weather(city)
            print(format_current(current))
            print()
            forecast = get_forecast(city)
            print(format_simple_forecast(forecast, entries=5))
            print("\n---\n")
        except WeatherAPIError as e:
            print("Error:", e)
