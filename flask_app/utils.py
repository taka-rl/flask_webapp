import json
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from typing import Any
from flask import abort, session, g
from flask_login import current_user

# API KEY OpenWeather
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
# API KEY ExchangeRate_API
ExchangeRate_API_KEY = os.getenv('ExchangeRate_API_KEY')
BASE_CURRENCY = 'JPY'
TARGET_CURRENCY = 'HUF'

ADMIN_NAME = os.getenv('ADMIN_NAME')


def load_translations(lang):
    try:
        with open(f'static/translations/{lang}.json', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # default to English if the file is not found
        with open(f'../static/translations/en.json', encoding='utf-8') as f:
            return json.load(f)


def with_translations(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        lang = session.get('lang', 'en')
        g.translations = load_translations(lang)
        return f(*args, **kwargs)
    return decorated_function


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # OnlyIf id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(code=403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def send_email(to_email, name, phone, subject, message):
    from_email = os.getenv('MYEMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    cc_email = None
    bcc_email = None

    # Create the email headers
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Thank you for your message!'

    if cc_email:
        msg['Cc'] = cc_email

    # Create header and footer messages
    header_message = (f'Dear {name},\n\n'
                      f'Thank you for your message!\n'
                      f'I will check your message and get back to you quickly!\n\n'
                      f'-------- Messages that you sent are as follows: --------\n'
                      f'Name: {name}\n'
                      f'Phone: {phone}\n'
                      f'Subject: {subject}\n'
                      f'Message: \n')

    footer_message = (f'\n--------------------------------------------------------\n\n'
                      f'Best regards,\n'
                      f'{ADMIN_NAME}\n'
                      f'{from_email}\n')

    # Combine messages
    message = header_message + message + footer_message

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    # Collect all recipients (to, cc, and bcc)
    recipients = [to_email]
    if cc_email:
        recipients += [cc_email]
    if bcc_email:
        recipients += [bcc_email]

    with smtplib.SMTP("smtp.gmail.com", timeout=60, port=587) as connection:
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=recipients,
            msg=msg.as_string()
        )


def get_currency_info() -> dict[str, str, float]:
    """
    Return the currency exchange rate between base currency and target currency through ExchangeRate API

    Returns:
        dict: the currency exchange information
    """
    import requests

    api_key = ExchangeRate_API_KEY

    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{BASE_CURRENCY}/{TARGET_CURRENCY}'

    # Get the information
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        currency_data = {'base_currency': BASE_CURRENCY, 'target_currency': TARGET_CURRENCY,
                         'exchange_rate': data['conversion_rate']}

        return currency_data
    else:
        # Print error message with status code
        print(f"Error: HTTP Status code: {response.status_code}")
        if response.status_code == 401:
            return "Error: Unauthorized: Check if your API key is correct."
        elif response.status_code == 404:
            return "Error: City not found: Please check the city name and try again."
        else:
            return "Error: An unexpected error occurred."


def get_weather_info(location: str) -> dict[str, Any]:
    """
    Return the weather information depending on the location through OpenWeather API
    About URL setting: https://openweathermap.org/current#builtin

    Parameters:
        location (str): the location

    Returns:
        dict: the weather information
    """

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