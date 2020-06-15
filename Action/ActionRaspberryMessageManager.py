import json

from BuzzerManager import BuzzerManager

class ActionRaspberryMessageManager(object):
    def __init__(self, client):

        self.client = client
        self.client.message_handler = self.on_message_handler
        self.buzzer_manager = BuzzerManager()

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        #person recognition by raspberry
        if message.topic == "action/buzzer":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["action"])
            print("message value:", new_value)

            if new_value == 1.0:
                self.buzzer_manager.buzzAct()