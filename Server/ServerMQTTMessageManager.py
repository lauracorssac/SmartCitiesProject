import json

class ServerMQTTMessageManager(object):

    def __init__(self, client):

        self.client = client
        self.client.message_handler = self.on_message_handler

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        #person recognition by raspberry
        if message.topic == "sensor/personRecognition":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["value"])
            print("message value:", new_value)

            if new_value == 1.0:
                action_message = '{"action": "%.2f"}' % 1.0
                self.client.publish("action/buzzer", action_message, 0, False)
