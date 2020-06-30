import json
import sys
import time

import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd()))

from Common.MQTTClientSerializer import MQTTClientSerializer
from ServerMQTTMessageManager import ServerMQTTMessageManager

should_end = False

def completion_handler():
    global should_end
    should_end = True

def main(argv):

    property_file_name = "ServerSettings.json"
    serializer = MQTTClientSerializer()
    mqtt_client = serializer.initialize_from_json(property_file_name)
    mqtt_client.start()
    manager = ServerMQTTMessageManager(mqtt_client, completion_handler)

    while not should_end:
        time.sleep(5)
        
    print("Ending program. Please wait.")
    mqtt_client.finalize()

# Call main function
if __name__ == "__main__":
    main(sys.argv[1:])
