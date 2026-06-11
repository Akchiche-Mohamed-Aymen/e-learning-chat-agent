import requests
from langchain.tools import tool
from json import load
@tool
def fetch_weather(city: str , convert_to_celsius: bool)->str:
    """returns the current weather in a given city."""
    try:
        url = f"""https://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&appid=66f4afc899fe0ee3d2e2d847ee431037"""
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        weather = int(response['list'][0]['main']['temp'])  
        if convert_to_celsius:
            weather = (weather - 32) * 5.0/9.0
            return weather 
        return f"The current weather in {city} is {weather}°F."
    except requests.exceptions.Timeout:
        return "Error: The request timed out."
    except requests.exceptions.ConnectionError:
        return "Error: Failed to connect to the server."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"An error occurred: {err}"


grade_data = load(open("grades.json", "r"))
@tool
def getGrade(student_name :str)->str:
    """Returns the grade of a student given their name."""
    student_name = student_name.lower()
    if student_name in grade_data.keys():
        return grade_data[student_name]
    else:
        return "Student not found"
def fehrenit_to_celsius(temp_f: float)->str:
    """Converts a temperature from Fahrenheit to Celsius."""
    temp_c = (temp_f - 32) * 5.0/9.0
    return temp_c
tools_list = [fetch_weather, getGrade  ]