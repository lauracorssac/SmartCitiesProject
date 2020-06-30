import json
import sys

class SensorRaspberryMessageManager(object):

    def __init__(self, client, completion_handler):
        self.client = client
        self.completion_handler = completion_handler
        self.client.message_handler = self.on_message_handler

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        if message.topic == "action/shutDown":
            self.completion_handler()
