import time
from rpi_ws281x import Color, PixelStrip, ws

# LED strip configuration:
LED_COUNT = 1 # Number of LED pixels.
LED_PIN = 13 # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10 # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1
# LED_STRIP = ws.SK6812_STRIP_RGBW
LED_STRIP = ws.SK6812W_STRIP

class LightManager(object):

    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.setup()

    def setup(self):
        self.strip.begin()
        self.strip.setPixelColor(0, Color(0, 0, 0))
        self.strip.show()

    def turn_light_on(self):
        self.strip.setPixelColor(0, Color(0, 255, 0))
        self.strip.show()

    def turn_light_off(self):
        self.strip.setPixelColor(0, Color(0, 0, 0))
        self.strip.show()
