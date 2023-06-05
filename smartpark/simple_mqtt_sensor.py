""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""

import mqtt_device
import json
import random

import time

class Sensor(mqtt_device.MqttDevice):

    @staticmethod
    def read_temperature() -> float:
        # not real
        # return float, min = 20 max = 40
        return random.random() * 20 + 20


    def on_detection(self, state):
        """Triggered when a detection occurs"""

        payload = {
            "temperature": self.read_temperature(),
            "state": state
        }
        
        self.client.publish('sensor', json.dumps(payload))

    def start_sensing(self):
        """ A blocking event loop that waits for detection events, in this
        case Enter presses"""
        while True:
            # print("Press E when 🚗 entered!")
            # print("Press X when 🚖 exited!")
            # detection = input("E or X> ").upper()
            time.sleep(random.randint(1,5))
            detection = random.choice(["E", "X"])
            print(detection)
            
            if detection == 'E':
                self.on_detection("enter")
            else:
                self.on_detection("exit")


if __name__ == '__main__':
    config1 = {'name': 'sensor',
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'entry'
              }
    # TODO: Read config from file

    sensor1 = Sensor(config1)


    print("Sensor initialised")
    sensor1.start_sensing()

