import json
import sys

class ActionRaspberryMessageManager(object):

    def __init__(self, client, light_manager, buzzer_manager):
        self.client = client
        self.client.message_handler = self.on_message_handler
        self.buzzer_manager = buzzer_manager
        self.light_manager = light_manager

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        if message.topic == "action/buzzer":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["action"])
            print("message value:", new_value)

            if new_value == 1.0:
                self.buzzer_manager.turn_buzzer_on()
            elif new_value == 0.0:
                self.buzzer_manager.turn_buzzer_off()

        if message.topic == "action/light":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["action"])
            print("message value:", new_value)

            if new_value == 1.0:
                self.light_manager.turn_light_on()
            if new_value == 0.0:
                self.light_manager.turn_light_off()


        if message.topic == "action/shutDown":
            raise ValueError("program ended")
