import json
import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))
from AI.Solver import Solver

class ServerMQTTMessageManager(object):

    def __init__(self, client, completion_handler):

        self.client = client
        self.completion_handler = completion_handler
        self.client.message_handler = self.on_message_handler
        self.solver = Solver()
        self.person_detected = False
        self.time_waited = False
        self.get_actions()

    def get_actions(self):

        response = self.solver.request()
        print("solver response", response)
        if "result" in response and "plan" in response["result"]:
            
            plan = response["result"]["plan"]
            action_cursor = 0
            
            while action_cursor < len(plan):
                print("action cursor", action_cursor)
                action = plan[action_cursor]
                if "name" in action: 
                    name = action["name"][1:-1]
                    action_contents = name.split(" ")
                    
                    if len(action_contents) >= 2:
                        action_name = action_contents[0]
                        print("action name = ", action_name)
                        action_object = action_contents[1]
                        print("action object = ", action_object)

                    if action_name == "turn-component-on":
                        if action_object == "buzzerobj":
                            self.turn_buzzer_on()
                        elif action_object == "lightobj":
                            self.turn_lights_on()
                        action_cursor += 1

                    elif action_name == "turn-actuator-off":
                        if action_object == "buzzerobj":
                            self.turn_buzzer_off()
                        elif action_object == "lightobj":
                            self.turn_lights_off()
                        action_cursor += 1

                    elif action_name == "wait-for-person":
                        if self.person_detected:
                            action_cursor += 1

                    elif action_name == "wait-for-while":
                        if self.time_waited:
                            action_cursor += 1

                    elif action_name == "turn-algorithm-off":
                        self.shut_down()
                        action_cursor += 1

    def on_message_handler(self, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        #person recognition by raspberry
        if message.topic == "sensor/personRecognition":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)

            new_value = float(msg_json["value"])
            print("person rec value:", new_value)
            if new_value == 1.0:
                self.person_detected  = True

        if message.topic == "sensor/time":
            message_string = message.payload.decode(encoding='UTF-8')
            msg_json = json.loads(message_string)
            new_value = int(msg_json["value"])
            print("time value:", new_value)
            self.time_waited = (new_value >= 90)


    def shut_down(self):
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/shutDown", action_message, 0, False)
        self.completion_handler()

    def turn_buzzer_on(self): 
        print("turning buzzer on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/buzzer", action_message, 0, False)

    def turn_lights_on(self): 
        print("turning lights on")
        action_message = '{"action": "%.2f"}' % 1.0
        self.client.publish("action/light", action_message, 0, False)

    def turn_buzzer_off(self): 
        print("turning buzzer off")
        action_message = '{"action": "%.2f"}' % 0.0
        self.client.publish("action/buzzer", action_message, 0, False)

    def turn_lights_off(self): 
        print("turning lights off")
        action_message = '{"action": "%.2f"}' % 0.0
        self.client.publish("action/light", action_message, 0, False)
