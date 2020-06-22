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
        self.old_time = 0
        self.time_changed = False

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        #person recognition by raspberry
        if message.topic == "sensor/personRecognition":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["value"])
            print("person rec value:", new_value)

            #executes post request only when a change in the state is detected 
            if self.old_value != new_value or self.time_changed:
                print("change of state detected, starting http")
                response = self.solver.request(new_value, self.old_time)
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
                                
                                elif action_name == "turn-system-off":
                                    self.shut_down()

            self.old_value = new_value

        if message.topic == "sensor/time":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)
            new_value = int(msg_json["value"])
            print("time value:", new_value)
            if self.old_time != new_value:
                self.time_changed = True
                self.old_time = new_value


    def shut_down(self):
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/shutDown", action_message, 0, False)
        raise ValueError("shut down")

    def turn_buzzer_on(self): 
        print("turning buzzer on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/buzzer", action_message, 0, False)

    def turn_lights_on(self): 
        print("turning lights on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/light", action_message, 0, False)
