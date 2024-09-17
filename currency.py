import os


# API KEY ExchangeRate_API
ExchangeRate_API_KEY = os.getenv('ExchangeRate_API_KEY')
BASE_CURRENCY = 'JPY'
TARGET_CURRENCY = 'HUF'


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