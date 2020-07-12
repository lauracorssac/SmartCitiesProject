import spidev
from time import sleep


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


# CODE FOR TESTING LIGHT SENSOR
obj = LightnessManager()
while True:
    print(obj.get_brightness_percentage())
    sleep(1)
