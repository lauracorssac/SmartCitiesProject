import spidev
from time import sleep

# Initialisiere Licht-Sensor auf Analogen-PIN 0
temp = 0

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000


def readadc(adcnum):
    # SPI-Daten auslesen
    r = spi.xfer2([1, 8+adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8)+r[2]
    return adcout


while True:
    value = readadc(temp)
    print("Value: " + str(value))
    sleep(1)
