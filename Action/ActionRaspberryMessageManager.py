import json
import sys

class ActionRaspberryMessageManager(object):

    def __init__(self, client, light_manager, buzzer_manager):
        self.client = client
        self.client.message_handler = self.on_message_handler
        self.buzzer_manager = buzzer_manager
        self.light_manager = light_manager

    def on_message_handler(self, message):
        print("on message topic: ", message.topic)

        if message.topic == "action/buzzer":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["action"])

            if new_value == 1.0:
                self.buzzer_manager.turn_buzzer_on()
            elif new_value == 0.0:
                self.buzzer_manager.turn_buzzer_off()

        elif message.topic == "action/LED":
            print("CAI NA MENSAGEM DO LEDZIN MAROTO")
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)
            new_value = float(msg_json["action"])
            print("new value", new_value)
            new_value = new_value if new_value < 100 else 100
            self.light_manager.set_light_brightness(new_value)
