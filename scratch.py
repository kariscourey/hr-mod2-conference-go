import requests

from events.keys import OPEN_WEATHER_API_KEY

city = "Philadelphia"
state = "PA"
country = "USA"
limit = 1

url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit={limit}&appid={OPEN_WEATHER_API_KEY}"

res = requests.get(url)
# print(res.json())

lat = res.json()[0]["lat"]
lon = res.json()[0]["lon"]

# print(lat, lon)

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}&units=imperial"

res = requests.get(url)

# print(res.json())
print(res.json()["weather"][0]["description"])

weather_desc = res.json()["weather"][0]["description"]
current_temp = res.json()["main"]["temp"]

print(weather_desc)
print(current_temp)
