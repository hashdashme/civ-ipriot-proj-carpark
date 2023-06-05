import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage
import mqtt_device
from config_parser import parse_config
from datetime import datetime
import json


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self.temperature = config['temperature']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.loop_forever()

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return available if available > 0 else 0

    def _publish_event(self):
        payload = {
            "time": datetime.now().strftime('%H:%M:%S'),
            "spaces": self.available_spaces,
            "temperature": self.temperature
        }
        print(payload)
        self.client.publish('display', json.dumps(payload))

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):        
        payload = msg.payload.decode()
        data = json.loads(payload)

        # update temperature from sensor
        self.temperature = data['temperature']

        if data['state'] == 'exit':
            self.on_car_exit()
        elif data['state'] == 'enter':
            self.on_car_entry()
        else:
            print('received invalid state!')

if __name__ == '__main__':
    config = {'name': "carpark-coordinator",
              'total-spaces': 130,
              'total-cars': 0,
              'temperature': 30,
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'entry',
              'is_stuff': False
              }
    # TODO: Read config from file
    car_park = CarPark(config)
    print("Carpark initialized")
