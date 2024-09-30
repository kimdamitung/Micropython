
from utime import sleep_ms
from gc import collect 
from machine import I2C

class SETUP:
    _CLR = 0x01
    _HOME = 0x02
    _ENTRY_MODE = 0x04
    _ENTRY_INC = 0x02
    _ON_CTRL = 0x08
    _ON_DISPLAY = 0x04
    _FUNCTION = 0x20
    _FUNCTION_2LINES = 0x08
    _FUNCTION_RESET = 0x30
    _DDRAM = 0x80
    def __init__(self, rows, cols):
        self.rows = rows
        if self.rows > 4:
            self.rows = 4
        self.cols = cols
        if self.cols > 40:
            self.cols = 40
        self.x = 0
        self.y = 0
        self.newROWS = False
        self.state = True
        self.showOFF()
        self.stateON()
        self.clear()
        self.write_cmd(self._ENTRY_MODE | self._ENTRY_INC)
        self.hide()
        self.showON()
    def clear(self):
        self.write_cmd(self._CLR)
        self.write_cmd(self._HOME)
        self.x = 0
        self.y = 0
    def hide(self):
        self.write_cmd(self._ON_CTRL | self._ON_DISPLAY)
    def showON(self):
        self.write_cmd(self._ON_CTRL | self._ON_DISPLAY)
    def showOFF(self):
        self.write_cmd(self._ON_CTRL)
    def stateON(self):
        self.state = True
        self.on()
    def move(self, x, y):
        self.x = x
        self.y = y
        address = x & 0x3f
        if y & 1:
            address += 0x40 
        if y & 2: 
            address += self.cols
        self.write_cmd(self._DDRAM | address)
    def character(self, char):
        if char == '\n':
            if self.newROWS:
                pass
            else:
                self.x = self.cols
        else:
            self.write_data(ord(char))
            self.x += 1
        if self.x >= self.cols:
            self.x = 0
            self.y += 1
            self.newROWS = (char != '\n')
        if self.y >= self.rows:
            self.y = 0
        self.move(self.x, self.y)
    def printf(self, string):
        for char in string:
            self.character(char)
    def on(self):
        pass
    def write_cmd(self, cmd):
        raise NotImplementedError
    def write_data(self, data):
        raise NotImplementedError

MASK_RS = 0x01
MASK_RW = 0x02 
MASK_E  = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA      = 4

class LCD1602(SETUP):
    def __init__(self, i2c, address, rows, cols):
        self.i2c = i2c
        self.address = address
        self.i2c.writeto(self.address, bytes([0]))
        sleep_ms(20)
        self.write_init(self._FUNCTION_RESET)
        sleep_ms(5)
        self.write_init(self._FUNCTION_RESET)
        sleep_ms(1)
        self.write_init(self._FUNCTION_RESET)
        sleep_ms(1)
        self.write_init(self._FUNCTION)
        sleep_ms(1)
        SETUP.__init__(self, rows, cols)
        cmd = self._FUNCTION
        if rows > 1:
            cmd |= self._FUNCTION_2LINES
        self.write_cmd(cmd)
        collect()
    def write_init(self, n):
        byte = ((n >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        collect()
    def on(self):
        self.i2c.writeto(self.address, bytes([1 << SHIFT_BACKLIGHT]))
        collect()
    def write_cmd(self, cmd):
        byte = ((self.state << SHIFT_BACKLIGHT) | (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        byte = ((self.state << SHIFT_BACKLIGHT) | ((cmd & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        if cmd <= 3:
            sleep_ms(5)
        collect()
    def write_data(self, data):
        byte = (MASK_RS | (self.state << SHIFT_BACKLIGHT) | (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        byte = (MASK_RS | (self.state << SHIFT_BACKLIGHT) | ((data & 0x0f) << SHIFT_DATA))      
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        collect()