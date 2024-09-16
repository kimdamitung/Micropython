import esp
esp.osdebug(0)
#import module micropython
import os
from machine import Pin, PWM
from utime import sleep, sleep_ms
from neopixel import NeoPixel
from package.controller.L298N import L298N
turn_error = NeoPixel(Pin(48, Pin.OUT), 1)
turn_error[0] = (0, 0, 0)
turn_error.write()
l298n = L298N(15, 7, 6, 5, 16, 4, 20000) #16, 4
print("L298N initialized")
print("Forward 25% speed")
l298n.forward(25)
sleep(5)
print("Backward 65% speed")
l298n.backward(65)
sleep(5)
print("Right turn 78% speed")
l298n.right(78)
sleep(5)
print("Left turn 12% speed")
l298n.left(12)
sleep(5)
l298n.stop()
print("Stopped")

while True:
    '''code'''
    pass