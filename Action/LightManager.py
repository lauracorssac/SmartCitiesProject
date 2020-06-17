import RPi.GPIO as GPIO
import time

PIN = 26 #DATA PIN

class LightManager(object):

    def __init__(self):
        self.setup()
        return

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.output(PIN, False) #light initially off

    def turn_light_on(self):
        GPIO.output(PIN, True) #turn light on
