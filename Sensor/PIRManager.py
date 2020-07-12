import time
import RPi.GPIO as GPIO


class PIRManager(object):

    def __init__(self, event_detected_callback, PIN):
        self.event_callback = event_detected_callback
        self.setup(PIN)

    def setup(self, PIN):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN)
        GPIO.add_event_detect(PIN, GPIO.RISING,
                              callback=self.event_callback)


#  FOLLOWING COMMENTED CODE IS AN EXEMPLE OF THIS CLASS USAGE

# def LIGHTS(pirPin):
#     """Turns LEDS On and Off"""
#     print("Motion Detected!")
#     time.sleep(2)
#
# print("Motion Sensor Alarm (CTRL+C to exit)")
# time.sleep(.2)
# print("Ready")
#
# obj = PIRManager(LIGHTS, 20)
#
# try:
#     while 1:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Quit")
#     GPIO.cleanup()
