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

def main():

    print("main fcuntion")
    property_file_name = "ActionRaspberrySettings.json"
    iot_manager = IoTGeneralManager()
    iot_manager.start()
    serializer = MQTTClientSerializer()
    mqtt_client = serializer.initialize_from_json(property_file_name)
    mqtt_client.start()
    light_manager = LightManager()
    buzzer_manager = BuzzerManager()
    manager = ActionRaspberryMessageManager(mqtt_client, light_manager, buzzer_manager)

    while True:
        try:
            if buzzer_manager.isOn:
                buzzer_manager.buzzAct()
            time.sleep(5)
        except:
            print("ending program")
            mqtt_client.finalize()
            iot_manager.stop()
            break


if __name__ == '__main__':
    main()
