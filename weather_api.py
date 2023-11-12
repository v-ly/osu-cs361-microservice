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
        self._air_pollution_url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}'

    def get_weather(self, request: json) -> json:
        """
        Returns the current weather information for specify city.
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: JSON
        """
        stringify_parameter = self._parameter_stringify(request)

        response = requests.get(self._weather_url.format(parameters=stringify_parameter, key=self._key))
        return response.json()

    def get_forecast(self, request: json) -> json:
        """
        Returns 5-day weather forecast for specify city.
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: JSON
        """
        stringify_parameter = self._parameter_stringify(request)

        response = requests.get(self._forecast_url.format(parameters=stringify_parameter, key=self._key))
        return response.json()

    def _get_lat_lon(self, request: json) -> dict:
        """
        Returns lat and lon for specify city.
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: dict
        """
        stringify_parameter = self._parameter_stringify(request)

        response = requests.get(self._geo_url.format(parameters=stringify_parameter, key=self._key))
        response_parsed = response.json()[0]

        return {'lat': response_parsed['lat'], 'lon': response_parsed['lon']}

    def get_air_pollution(self, request: json) -> json:
        """
        Returns the air pollution data for specify city.
        :param request: (JSON) cityName [required], state [optional], country [optional]
        :return: json
        """
        request_lat_lon = self._get_lat_lon(request)

        response = requests.get(
            self._air_pollution_url.format(lat=request_lat_lon['lat'], lon=request_lat_lon['lon'], key=self._key)
        )

        return response.json()

    def _parameter_stringify(self, request: json) -> str:
        """
        Convert request JSON into string to fit in URL parameters.
        :param request: JSON cityName [required], state [optional], country [optional]
        :return: str
        """

        request_parsed = json.loads(request)

        parameter = ''

        if 'cityName' not in request_parsed:
            return parameter
        else:
            parameter = self.url_formatting(request_parsed['cityName'])

            if 'state' in request_parsed:
                parameter = self.url_formatting(request_parsed['state'])

            if 'state' in request_parsed and 'country' in request_parsed:
                parameter = self.url_formatting(request_parsed['country'])

        return parameter

    @staticmethod
    def url_formatting(string: str) -> str:
        """
        Convert spaces to URL friendly format.
        :param string: Any string.
        :return: str
        """
        return string.replace(' ', '%20')


if __name__ == '__main__':

    weather_api = WeatherAPI()

    parameters = json.dumps({'cityName': 'san francisco', 'state': 'california'})
    print(weather_api.get_weather(parameters))
    print(weather_api.get_forecast(parameters))
    print(weather_api.get_air_pollution(parameters))
