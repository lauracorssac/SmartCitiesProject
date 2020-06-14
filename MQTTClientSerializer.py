
from MQTTClient import MQTTClient
import json

CONFIG = "config"
TOPICS = "topics"
BROKER_HOST = "brokerHost"
BROKER_PORT = "brokerPort"
SUBSCRIBE = "subscribe"

class MQTTClientSerializer(object):

    def initialize_from_json(self, jsonFile):

        hostname = ""
        port = 0
        topics_to_subscribe = []
        client_id = "id_client" #todo: change to something better

        with open(jsonFile) as f:
            data_dict = json.load(f)

            hostname = data_dict[CONFIG][BROKER_HOST]
            port = int(data_dict[CONFIG][BROKER_PORT])
            topics_to_subscribe = data_dict[TOPICS][SUBSCRIBE]

            return MQTTClient(hostname, port, client_id, topics_to_subscribe)

        return None
