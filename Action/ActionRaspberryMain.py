import time
from datetime import datetime
import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))

from Common.MQTTClientSerializer import MQTTClientSerializer
from ActionRaspberryMessageManager import ActionRaspberryMessageManager

def main():

    print("main fcuntion")
    property_file_name = "ActionRaspberrySettings.json"
    serializer = MQTTClientSerializer()
    mqtt_client = serializer.initialize_from_json(property_file_name)
    mqtt_client.start()
    manager = ActionRaspberryMessageManager(mqtt_client)

    while True:
        time.sleep(5)


if __name__ == '__main__':
    main()
