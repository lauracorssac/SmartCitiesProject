import time
from datetime import datetime
import sys
import os

sys.path.insert(1, os.path.dirname(os.getcwd()))

from Common.MQTTClientSerializer import MQTTClientSerializer
from ActionRaspberryMessageManager import ActionRaspberryMessageManager
from Common.IoTGeneralManager import IoTGeneralManager
from BuzzerManager import BuzzerManager
from LightManager import LightManager


should_end = False

def completion_handler():
    global should_end
    should_end = True

def main():

    property_file_name = "ActionRaspberrySettings.json"
    iot_manager = IoTGeneralManager()
    iot_manager.start()
    serializer = MQTTClientSerializer()
    mqtt_client = serializer.initialize_from_json(property_file_name)
    mqtt_client.start()
    light_manager = LightManager()
    buzzer_manager = BuzzerManager()
    manager = ActionRaspberryMessageManager(mqtt_client, light_manager, buzzer_manager, completion_handler)

    while not should_end:
        if buzzer_manager.is_on:
            buzzer_manager.buzzAct()
        time.sleep(5)
       
    print("Ending program. Please Wait.")
    mqtt_client.finalize()
    iot_manager.stop()


if __name__ == '__main__':
    main()
