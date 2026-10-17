import json
from urllib.parse import urlencode
from urllib.request import urlopen

city = input("your city: ").strip()

if not city:
    raise SystemExit("enter a city.")

try:
    params = urlencode({
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    })
    url = f"https://geocoding-api.open-meteo.com/v1/search?{params}"

    with urlopen(url, timeout=10) as response:
        places = json.load(response).get("results", [])

    if not places:
        raise SystemExit("City not found.")

    place = places[0]

    weather_params = urlencode({
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    })
    weather = f"https://api.open-meteo.com/v1/forecast?{weather_params}"

    with urlopen(weather, timeout=10) as response:
        current = json.load(response)["current"]

    print(f"\nWeather in {place['name']}:")
    print(f"Temperature: {current['temperature_2m']} °C")
    print(f"Wind speed: {current['wind_speed_10m']} km/h")
    print(f"Weather code: {current['weather_code']}")

except (OSError, KeyError, ValueError) as error:
    print(f"Could not get the weather: {error}")