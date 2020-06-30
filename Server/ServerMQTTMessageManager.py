import json
import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))
from AI.Solver import Solver
from collections import defaultdict

class ServerMQTTMessageManager(object):

    def __init__(self, client, completion_handler):

        self.client = client
        self.completion_handler = completion_handler
        self.client.message_handler = self.on_message_handler
        self.solver = Solver()
        self.person_detected = False
        self.time_waited = False
        self.action_cursor = 0

        self.server_actions = {
            "turn-component-on": {
                "buzzerobj": self.turn_buzzer_on,
                "lightobj": self.turn_lights_on
            },
            "turn-actuator-off": {
                "buzzerobj": self.turn_buzzer_off,
                "lightobj": self.turn_lights_off
            },
             "wait-for-person": {
                "bouglar": self.wait_for_person
            },
            "wait-for-while": {
                "bouglar": self.wait_for_while
            },
            "turn-algorithm-off": {
                "algorithmobj": self.shut_down
            }
        }

        self.get_actions()

    def get_actions(self):

        response = self.solver.request()
        if "result" in response and "plan" in response["result"]:
            
            plan = response["result"]["plan"]
            
            while self.action_cursor < len(plan):
                action = plan[self.action_cursor]
                print("current action", self.action_cursor)
                if "name" in action: 
                    name = action["name"][1:-1]
                    action_contents = name.split(" ")
                    
                    if len(action_contents) >= 2:
                        action_name = action_contents[0]
                        action_object = action_contents[1]
                        self.server_actions[action_name][action_object]()

    def on_message_handler(self, message):
        print("on message topic: ", message.topic)

        # person recognition status by raspberry
        if message.topic == "sensor/personRecognition":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["value"])
            print("person rec value:", new_value)
            if new_value == 1.0:
                self.person_detected  = True

        # time measured by raspberry since person was detected
        if message.topic == "sensor/time":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)
            new_value = int(msg_json["value"])
            
            # waits for 90 seconds
            self.time_waited = (new_value >= 90)

    def shut_down(self):
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/shutDown", action_message, 0, False)
        self.completion_handler()
        self.action_cursor += 1

    def turn_buzzer_on(self): 
        print("turning buzzer on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/buzzer", action_message, 0, False)
        self.action_cursor += 1

    def turn_lights_on(self): 
        print("turning lights on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/light", action_message, 0, False)
        self.action_cursor += 1

    def turn_buzzer_off(self): 
        print("turning buzzer off")
        action_message = '{"action": "%.2f"}' % 0.0
        self.client.publish("action/buzzer", action_message, 0, False)
        self.action_cursor += 1

    def turn_lights_off(self): 
        print("turning lights off")
        action_message = '{"action": "%.2f"}' % 0.0
        self.client.publish("action/light", action_message, 0, False)
        self.action_cursor += 1

    def wait_for_person(self):
        if self.person_detected:
            self.action_cursor += 1

    def wait_for_while(self):
        if self.time_waited:
            self.action_cursor += 1
