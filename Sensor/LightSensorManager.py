import spidev
import sys
import os
import time
sys.path.insert(1, os.path.dirname(os.getcwd()))
from Common.MQTTClientSerializer import MQTTClientSerializer
from SensorMQTTMessageManager import SensorMQTTMessageManager
from Common.IoTGeneralManager import IoTGeneralManager



class LightnessManager(object):

    def __init__(self):
        self.setup()

    def setup(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 10000

    def get_brightness_percentage(self):
        # SPI-Daten auslesen
        r = self.spi.xfer2([1, 8 << 4, 0])
        adcout = ((r[1] & 3) << 8)+r[2]
        percentage_of_light = adcout*100/620
        return percentage_of_light


property_file_name = "SensorRaspberrySettings.json"
serializer = MQTTClientSerializer()
mqtt_client = serializer.initialize_from_json(property_file_name)
mqtt_client.start()
message_manager = SensorMQTTMessageManager(mqtt_client)
light_sensor = LightnessManager()


while True:
    value = light_sensor.get_brightness_percentage()
    print(value)
    
    message_manager.send_brightness(value)
    time.sleep(5)
