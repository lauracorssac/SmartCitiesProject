import RPi.GPIO as GPIO


class LightManager(object):

    def __init__(self, port_number):
        self.setup(port_number)

    def setup(self, port_number):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port_number, GPIO.OUT)
        self.led = GPIO.PWM(port_number, 500)
        self.led.start(0)

    def set_light_brightness(self, brightness_percentage):
        self.led.ChangeDutyCycle(brightness_percentage)
