import requests

def fetch_weather(city='Ouargla'):
    """returns the current weather in a given city."""
    try:
        url = f"""https://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&appid=66f4afc899fe0ee3d2e2d847ee431037"""
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        weather = response['list'][0]['main']['temp']
        return f"The current weather in {city} is {weather}°F."
    except requests.exceptions.Timeout:
        return "Error: The request timed out."
    except requests.exceptions.ConnectionError:
        return "Error: Failed to connect to the server."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"An error occurred: {err}"


