import json
import sys
from BuzzerManager import BuzzerManager
from LightManager import LightManager

class ActionRaspberryMessageManager(object):

    def __init__(self, client):
        self.client = client
        self.client.message_handler = self.on_message_handler
        self.buzzer_manager = BuzzerManager()
        self.light_manager = LightManager()

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        if message.topic == "action/buzzer":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["action"])
            print("message value:", new_value)

            if new_value == 1.0:
                self.buzzer_manager.buzzAct()
                self.light_manager.turn_light_on()

        if message.topic == "action/light":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["action"])
            print("message value:", new_value)

            if new_value == 1.0:
                self.light_manager.turn_light_on()


        if message.topic == "action/shutDown":
            raise ValueError("program ended")
