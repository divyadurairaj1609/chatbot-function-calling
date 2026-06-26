import requests

def get_weather(city):
    """Get current weather for a city"""
    
    # Using Open-Meteo API — completely free, no API key needed!
    # First get coordinates for the city
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    
    geo_response = requests.get(geocoding_url)
    geo_data = geo_response.json()
    
    # Check if city was found
    if not geo_data.get("results"):
        return f"City '{city}' not found. Please try another city name."
    
    # Get coordinates
    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]
    country = location.get("country", "")
    
    # Get weather using coordinates
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    current = weather_data["current"]
    
    # Weather code descriptions
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Icy fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight showers",
        81: "Moderate showers",
        82: "Violent showers",
        95: "Thunderstorm",
        99: "Thunderstorm with hail"
    }
    
    weather_code = current.get("weather_code", 0)
    description = weather_codes.get(weather_code, "Unknown")
    
    # Return weather info as a clean string
    return f"""
Weather in {location['name']}, {country}:
- Temperature: {current['temperature_2m']}°C
- Condition: {description}
- Humidity: {current['relative_humidity_2m']}%
- Wind Speed: {current['wind_speed_10m']} km/h
"""