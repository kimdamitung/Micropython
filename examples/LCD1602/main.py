import esp
esp.osdebug(0)
#import module micropython
from package.display.LCD.LCD1602 import LCD1602
from machine import I2C, Pin

i2c = I2C(0, sda = Pin(8, Pin.OUT, Pin.PULL_UP), scl = Pin(9, Pin.OUT, Pin.PULL_UP), freq = 400000)
address = i2c.scan()
lcd1602 = LCD1602(i2c, address[0], 2, 16)
lcd1602.clear()
lcd1602.printf('Nguyen Duy Tung')
lcd1602.clear()
lcd1602.printf(f'Nguyen Duy Tung{199}\nKimdami')
while True:
    '''code'''
    pass