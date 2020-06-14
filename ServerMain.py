import json
import sys
import time

from MQTTClientSerializer import MQTTClientSerializer
from MQTTMessageManager import MQTTMessageManager


def main(argv):

    property_file_name = "ServerSettings.json"
    serializer = MQTTClientSerializer()
    mqtt_client = serializer.initialize_from_json(property_file_name)
    mqtt_client.start()
    manager = MQTTMessageManager(mqtt_client)

    while True:
        time.sleep(5)



# Call main function
if __name__ == "__main__":
    main(sys.argv[1:])
