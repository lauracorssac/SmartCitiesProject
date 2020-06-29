import RPi.GPIO as GPIO
import time

PD = 15 #DATA PIN

class BuzzerManager(object):

    def __init__(self):
        self.is_on = False
        self.buzzer_setup()
        return

    def turn_buzzer_on(self):
        self.is_on = True
        
    def turn_buzzer_off(self):
        self.is_on = False

    def buzzer_setup(self):
        GPIO.setup(PD, GPIO.OUT)
        GPIO.output(PD, 0)

    def buzzAct(self):
        for i in range(3):
            for i in range(100,500,20):
                self.buzz(10,500-i+100)

    def buzz(self, duration, freq):
    	GPIO.output(PD, 0)
    	for i in range(1,duration):
    		GPIO.output(PD, 1)
    		time.sleep(0.001)
    		GPIO.output(PD, 0)
    		time.sleep(1.0/freq)
    	GPIO.output(PD, 0)
