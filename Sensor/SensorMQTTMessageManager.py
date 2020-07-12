class SensorMQTTMessageManager(object):

    def __init__(self, client):
        self.client = client

    def send_person_rec_status(self, new_value):
        message = '{"value": "%.2f"}' % new_value
        self.client.publish(topic="sensor/personRecognition", payload=message,
                            qos=0, retain=False)

    def send_time(self, new_time):
        message = '{"value": "%d"}' % new_time
        self.client.publish(topic="sensor/time", payload=message, qos=0,
                            retain=False)

    def send_brightness(self, brightness_percentage):
        message = '{"value": "%d"}' % brightness_percentage
        self.client.publish(topic="sensor/brightness", payload=message,
                            qos=0, retain=False)
