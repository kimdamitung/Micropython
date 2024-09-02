import esp
esp.osdebug(0)
#import module micropython
from package.io.PCF.PCF8575 import PCF8575
from utime import sleep
from machine import I2C, Pin

i2c = I2C(0, sda = Pin(8, Pin.OUT, Pin.PULL_UP), scl = Pin(9, Pin.OUT, Pin.PULL_UP), freq = 400000)
address = i2c.scan()
pcf8575 = PCF8575(i2c, address[0])
keyboard = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]
keypad = {
    (0, 0): 'Nguyen Duy Tung', (0, 1): 'Nguyen Huy Thai', (0, 2): 'Nguyen Tuan Phat', (0, 3): 'Tran Hoang Hong Hai',
    (1, 0): 'Nguyen Long Hoang An', (1, 1): 'Nguyen Quoc Huy', (1, 2): 'Nguyen Minh Quang', (1, 3): 'La Ky Nguyen',
    (2, 0): 'Tran Khoi Nguyen', (2, 1): 'Nguyen Khac Son', (2, 2): 'Do Manh Dung', (2, 3): 'Nguyen Son Phu',
    (3, 0): 'Tran Thi Ngoc Hoa', (3, 1): 'Nguyen Van Danh', (3, 2): 'Nguyen Dac Hop', (3, 3): 'Doan Manh Tu'
}
led = pcf8575.PIN(10)
led.value = 0
sleep(1)
led.value = 1
while True:
    '''code'''
    # read button character
    key = pcf8575.setBoard16bit(keyboard)
    # read button dictionaries
    # key = pcf8575.dictionaries(keypad)
    if key:
        print(f"Key pressed: {key}")