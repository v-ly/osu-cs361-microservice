# Not included in repository is config.py
# Create and validate account on to https://openweathermap.org/
# Generate an API key in "My API Keys"


from config import api_key
import requests
import json


class WeatherAPI:
    def __init__(self, key: str = api_key):
        self._key = key
        self._weather_url = "https://api.openweathermap.org/data/2.5/weather?q={parameters}&appid={key}&units=imperial"

    def get_weather(self, request: json) -> json:
        """
        Returns the current weather information.
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: JSON
        """
        request_parsed = json.loads(request)
        parameters = ''
        if 'cityName' in request_parsed:
            parameters = self.url_formatting(request_parsed['cityName'])
        if 'state' in request_parsed:
            parameters = self.url_formatting(request_parsed['state'])
        if 'country' in request_parsed:
            parameters = self.url_formatting(request_parsed['country'])

        response = requests.get(self._weather_url.format(parameters=parameters, key=self._key))
        print(response.json())

    @staticmethod
    def url_formatting(string:str) -> str:
        return string.replace(' ', '%20')


if __name__ == '__main__':

    weather_api = WeatherAPI()

    parameters = json.dumps({'cityName':'san francisco'})
    weather_api.get_weather(parameters)
