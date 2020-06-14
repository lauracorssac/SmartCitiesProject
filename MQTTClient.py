#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import paho.mqtt.client as mqtt
import time
import os
from datetime import datetime
import json

class MQTTClient(object):

    def __init__(self, hostname, port, client_id, topics_to_subscribe):
        self.hostname = hostname
        self.port = port
        self.topics_to_subscribe = topics_to_subscribe

        # Create MQTT client
        self.client = mqtt.Client(client_id=client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)

        # Register callback functions
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected successfully with result code " + str(rc))
        print("topics", self.topics_to_subscribe)
        #subscribe to person rec topic
        for topic in self.topics_to_subscribe:
            self.subscribe(topic + "/#")

    def _on_message(self, client, userdata, message):
        # Convert message payload to string
        print("on message topic: ", message.topic)

        if message.topic in self.topics_to_subscribe:
            self.message_handler(message)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload, qos, retain):
        self.client.publish(topic, payload, qos, retain)

    def start(self):
        # Start MQTT client
        self.client.connect(self.hostname, self.port, 60)
        self.client.loop_start()

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
