import zmq
import sys
import time
import json
from weather_api import WeatherAPI


class WeatherMicroservice:

    def __init__(self, port: str):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.bind("tcp://*:%s" % port)
        self._weather_api = WeatherAPI()

    def run(self):
        while True:
            get_request = self._socket.recv_json()
            request = json.loads(get_request)
            if request['function'] == 'weather':
                print("Request for Current Weather")
                parameter = self._socket.recv_json()
                current_weather = self._weather_api.get_weather(request=parameter)
                self._socket.send_json(current_weather)
            elif request['function'] == 'forecast':
                print("Request for Forecast")
                parameter = self._socket.recv_json()
                current_weather = self._weather_api.get_forecast(request=parameter)
                self._socket.send_json(current_weather)
            elif request['function'] == 'air_pollution':
                print("Request for Air Pollution")
                parameter = self._socket.recv_json()
                current_weather = self._weather_api.get_air_pollution(request=parameter)
                self._socket.send_json(current_weather)
            time.sleep(1)


if __name__ == '__main__':
    server = WeatherMicroservice(sys.argv[1])
    server.run()
