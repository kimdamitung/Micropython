import esp
esp.osdebug(0)
#import module micropython
from package.display.OLED.OLED_096 import OLED_096
from machine import I2C, Pin

i2c = I2C(0, sda = Pin(8, Pin.OUT, Pin.PULL_UP), scl = Pin(9, Pin.OUT, Pin.PULL_UP), freq = 400000)
address = i2c.scan()
oled = OLED_096(128, 64, i2c, address[0])
oled.fill(0)
oled.text("Hello, OLED!", 0, 0)
while True:
    '''code'''
    pass