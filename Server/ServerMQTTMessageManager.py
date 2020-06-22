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
        self.old_value = 0.0

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        #person recognition by raspberry
        if message.topic == "sensor/personRecognition":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["value"])
            print("message value:", new_value)

            #executes post request only when a change in the state is detected 
            if old_value != new_value: #TODO: USE THE VALUE
                print("change of state detected, starting http")
                response = self.solver.request(new_value)
                if "result" in response and "plan" in response["result"]:
                    plan = response["result"]["plan"]
                    for action in plan:
                        if "name" in action: 
                            name = action["name"][1:-1]
                            action_contents = name.split(" ")
                            if len(action_contents) >= 3:
                                action_name = action_contents[0]
                                action_object = action_contents[2]
                                if action_name == "turn-actuator-on":
                                    if action_object == "buzzer-obj":
                                        self.turn_buzzer_on()
                                    elif action_object == "light-obj":
                                        self.turn_lights_on()

            old_value = new_value

    def turn_buzzer_on(self): 
        print("turning buzzer on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/buzzer", action_message, 0, False)
        #self.client.publish("action/shutDown", action_message, 0, False)
        #raise ValueError("shut down")

    def turn_lights_on(self): 
        print("turning lights on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/light", action_message, 0, False)
        #raise ValueError("shut down")
