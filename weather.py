from typing import Any


# API KEY
# OpenWeather
WEATHER_API_KEY = 'Replace with your API key'

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

    api_key = WEATHER_API_KEY  # Replace 'your_api_key_here' with your actual OpenWeatherMap API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    # Get the information
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        weather_data = {'temperature': data['main']['temp'], 'wind_speed': data['wind']['speed'],
                        'pressure': data['main']['pressure'], 'humidity': data['main']['humidity'],
                        'description': data['weather'][0]['description']}

        return weather_data
    else:
        # Print error message with status code
        print(f"Error: Unable to fetch data for {location}. HTTP Status code: {response.status_code}")
        if response.status_code == 401:
            print("Unauthorized: Check if your API key is correct.")
        elif response.status_code == 404:
            print("City not found: Please check the city name and try again.")
        else:
            print("An unexpected error occurred.")