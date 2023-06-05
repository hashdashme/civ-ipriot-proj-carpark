import mqtt_device
import time
import os
import json

class Display(mqtt_device.MqttDevice):
    """Displays the number of cars and the temperature"""
    def __init__(self, config):
        super().__init__(config)
        self.spaces = None

        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.client.loop_forever()


    def display(self, data):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('-' + '=-' * 10)
        for i, v in data.items():
            print(f"{i.capitalize()}:", end="")

            if i == 'temperature':
                print(f"\t{v:.1f}")                    
            elif i == 'spaces' and self.spaces is not None:
                delta = v - self.spaces

                print(f"\t\t{v} ({'+' if delta > 0 else ''}{delta})")
                self.spaces = int(v)
            else:
                print(f"\t\t{v}")
            
            # handle spaces = None
            if not self.spaces and i == 'spaces':
                self.spaces = int(v)

        print('-' + '=-' * 10)

    def on_message(self, client, userdata, msg):
       message = msg.payload.decode()
       data = json.loads(message)
       
       self.display(data)
if __name__ == '__main__':
    config = {'name': 'display',
     'location': 'L306',
     'topic-root': "lot",
     'broker': 'localhost',
     'port': 1883,
     'topic-qualifier': 'na'
     }
    # TODO: Read config from file
    display = Display(config)

