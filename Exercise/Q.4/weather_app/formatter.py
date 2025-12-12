from datetime import datetime

def format_current(data: dict) -> str:
    name = data.get("name", "Unknown")
    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    temp = main.get("temp")
    feels = main.get("feels_like")
    hum = main.get("humidity")
    desc = weather.get("description", "").capitalize()
    wind = data.get("wind", {}).get("speed")
    lines = [
        f"Weather for {name}:",
        f"  {desc}",
        f"  Temperature: {temp}°",
        f"  Feels like: {feels}°",
        f"  Humidity: {hum}%",
        f"  Wind speed: {wind} m/s"
    ]
    return "\n".join(lines)

def format_simple_forecast(forecast_json: dict, entries: int = 5) -> str:
    # forecast_json['list'] contains 3-hourly entries
    items = forecast_json.get("list", [])[:entries]
    lines = ["Forecast (next entries):"]
    for it in items:
        dt = datetime.fromtimestamp(it['dt'])
        desc = it['weather'][0]['description'].capitalize()
        temp = it['main']['temp']
        lines.append(f"  {dt.strftime('%Y-%m-%d %H:%M')} | {desc:20} | {temp}°")
    return "\n".join(lines)
