import requests

api_key = "f034f63fd8b285d7c6bd118dd32eb1cc"   

city = input("Enter city name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)

print("Status:", response.status_code)

weather = response.json()

# Check for errors first
if response.status_code != 200:
    print("Error:", weather["message"])
else:
    print("Temperature:", weather["main"]["temp"], "°C")
    print("Humidity:", weather["main"]["humidity"], "%")
    print("Wind Speed:", weather["wind"]["speed"], "m/s")
