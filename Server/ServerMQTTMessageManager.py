import json
import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))
from AI.Solver import Solver

class ServerMQTTMessageManager(object):

    def __init__(self, client):

        self.client = client
        self.client.message_handler = self.on_message_handler
        self.solver = Solver()

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

                response = self.solver.request(new_value)
                print("response", response)
                return
                
                #action_message = '{"action": "%.2f"}' % 1.0
                #self.client.publish("action/buzzer", action_message, 0, False)
                #self.client.publish("action/shutDown", action_message, 0, False)
                #raise ValueError("shut down")
