import json
import sys

class SensorRaspberryMessageManager(object):

    def __init__(self, client):
        self.client = client
        self.client.message_handler = self.on_message_handler

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        if message.topic == "action/shutDown":
            sys.exit(0)
