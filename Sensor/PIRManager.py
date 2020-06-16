import RPi.GPIO as GPIO
import time

PIN = 15 #DATA PIN

class PIRManager(object):

    def __init__(self, event_detected_callback):
        self.event_detected_callback = self.event_detected_callback
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.add_event_detect(PIN, GPIO.RISING, callback=event_detected, bouncetime=100)

    def event_detected():
        print("motion was detected")
        GPIO.cleanup() #stops receiving events after first motion was detected
        self.event_detected_callback()
