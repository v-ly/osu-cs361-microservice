# Not included in repository is config.py
# Create and validate account on to https://openweathermap.org/
# Generate an API key in "My API Keys"

# Citation for the following function: Weather API Data
# Date: 2023-11-11
# Adapted from: openweathermap.org example
# Source URL:
#   https://openweathermap.org/current#data
#   https://openweathermap.org/forecast5#name5
#   https://openweathermap.org/api/geocoding-api#direct_name


from config import api_key
import requests
import json


class WeatherAPI:
    def __init__(self, key: str = api_key):
        self._key = key
        self._weather_url = "https://api.openweathermap.org/data/2.5/weather?q={parameters}&appid={key}&units=imperial"
        self._forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?q={parameters}&appid={key}&units=imperial'
        self._geo_url = 'http://api.openweathermap.org/geo/1.0/direct?q={parameters}&limit=1&appid={key}'

    def get_weather(self, request: json) -> json:
        """
        Returns the current weather information.
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: JSON
        """
        request_parsed = json.loads(request)
        request_parameters = ''
        if 'cityName' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['cityName'])
        if 'state' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['state'])
        if 'country' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['country'])

        response = requests.get(self._weather_url.format(parameters=request_parameters, key=self._key))
        print(response.json())

    def get_forecast(self, request: json) -> json:
        """
        Returns 5-day weather forecast.
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: JSON
        """
        request_parsed = json.loads(request)
        request_parameters = ''
        if 'cityName' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['cityName'])
        if 'state' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['state'])
        if 'country' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['country'])

        response = requests.get(self._forecast_url.format(parameters=request_parameters, key=self._key))
        print(response.json())

    def _get_lat_lon(self, request: json) -> json:
        """
        Returns lat and lon for specify city
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: json
        """
        request_parsed = json.loads(request)
        request_parameters = ''
        if 'cityName' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['cityName'])
        if 'state' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['state'])
        if 'country' in request_parsed:
            request_parameters = self.url_formatting(request_parsed['country'])

        response = requests.get(self._geo_url.format(parameters=request_parameters, key=self._key))
        response_parsed = response.json()[0]

        return json.dumps({'lat': response_parsed['lat'], 'long': response_parsed['lon']})

    @staticmethod
    def url_formatting(string:str) -> str:
        return string.replace(' ', '%20')


if __name__ == '__main__':

    weather_api = WeatherAPI()

    parameters = json.dumps({'cityName': 'san francisco'})
    # weather_api.get_weather(parameters)
    # weather_api.get_forecast(parameters)
    print(weather_api._get_lat_lon(parameters))
