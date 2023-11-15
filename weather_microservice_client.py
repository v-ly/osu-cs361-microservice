import zmq
import sys
import json
import time


class WeatherMicroserviceClient:

    def __init__(self, port: str):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.connect("tcp://localhost:%s" % port)

    def get_weather(self, parameter: json):
        self._socket.send_json(json.dumps({'function': 'weather'}))
        self._socket.send_json(parameter)
        response = self._socket.recv_json()
        print(response)

    def get_forecast(self, parameter: json):
        self._socket.send_json(json.dumps({'function': 'forecast'}))
        self._socket.send_json(parameter)
        response = self._socket.recv_json()
        print(response)

    def get_air_pollution(self, parameter: json):
        self._socket.send_json(json.dumps({'function': 'air_pollution'}))
        self._socket.send_json(parameter)
        response = self._socket.recv_json()
        print(response)


if __name__ == '__main__':
    client = WeatherMicroserviceClient(sys.argv[1])

    print("======================================")
    location = json.dumps({'cityName': 'seattle'})
    client.get_weather(location)
    time.sleep(5)
    print("======================================")


    print("======================================")
    location = json.dumps({'cityName': 'san francisco'})
    client.get_forecast(location)
    time.sleep(5)
    print("======================================")

    print("======================================")
    location = json.dumps({'cityName': 'new york'})
    client.get_air_pollution(location)
    print("======================================")