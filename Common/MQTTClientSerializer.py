import sys
import os

sys.path.insert(1, os.path.dirname(os.getcwd()))

from Common.MQTTClient import MQTTClient
import json
from datetime import datetime

CONFIG = "config"
TOPICS = "topics"
BROKER_HOST = "brokerHost"
BROKER_PORT = "brokerPort"
SUBSCRIBE = "subscribe"
ID = "id"

class MQTTClientSerializer(object):

    def initialize_from_json(self, jsonFile):

        hostname = ""
        port = 0
        topics_to_subscribe = []

        with open(jsonFile) as f:

            data_dict = json.load(f)
            hostname = data_dict[CONFIG][BROKER_HOST]
            port = int(data_dict[CONFIG][BROKER_PORT])
            topics_to_subscribe = data_dict[TOPICS][SUBSCRIBE]
            client_id = data_dict[CONFIG][ID] + (datetime.utcnow().strftime('%H_%M_%S'))

            return MQTTClient(hostname, port, client_id, topics_to_subscribe)

        return None
