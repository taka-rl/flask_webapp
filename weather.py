from typing import Any
import os


# API KEY OpenWeather
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


def get_weather_info(location: str) -> dict[str, Any]:
    """
    Return the weather information depending on the location through OpenWeather API
    About URL setting: https://openweathermap.org/current#builtin

    Parameters:
        location (str): the location

    Returns:
        dict: the weather information
    """
    import requests

    api_key = WEATHER_API_KEY
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    # Get the information
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        print(data)

        weather_data = {'temperature': data['main']['temp'],
                        'max_temperature': data['main']['temp_max'],
                        'min_temperature': data['main']['temp_min'],
                        'feel_temperature': data['main']['feels_like'],
                        'wind_speed': data['wind']['speed'],
                        'pressure': data['main']['pressure'],
                        'humidity': data['main']['humidity'],
                        'description': data['weather'][0]['description']}

        return weather_data
    else:
        # Print error message with status code
        print(f"Error: Unable to fetch data for {location}. HTTP Status code: {response.status_code}")
        if response.status_code == 401:
            return "Error: Unauthorized: Check if your API key is correct."
        elif response.status_code == 404:
            return "Error: City not found: Please check the city name and try again."
        else:
            return "Error: An unexpected error occurred."