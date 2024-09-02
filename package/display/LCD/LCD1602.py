
from utime import sleep_ms
from gc import collect # type: ignore
from machine import I2C

class SETUP:
    """
        Base class for controlling an LCD display
    Raises:
        NotImplementedError: None
        NotImplementedError: None
    """
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
    def __init__(self, rows: int, cols: int):
        """
            Initializes the LCD with the given number of rows and columns.
        Args:
            rows (integer): number of rows in the LCD
            cols (integer): number of columns in the LCD
        """
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
        """
            CLear the display and return the cursor to the LCD
        """
        self.write_cmd(self._CLR)
        self.write_cmd(self._HOME)
        self.x = 0
        self.y = 0
    def hide(self):
        """
            Hide the cursor
        """
        self.write_cmd(self._ON_CTRL | self._ON_DISPLAY)
    def showON(self):
        """
            Turn on the display LCD
        """
        self.write_cmd(self._ON_CTRL | self._ON_DISPLAY)
    def showOFF(self):
        """
            Turn off the display LCD
        """
        self.write_cmd(self._ON_CTRL)
    def stateON(self):
        """
            Sets the display state to ON and initializes the display.
        """
        self.state = True
        self.on()
    def move(self, x, y):
        """
            Moves the cursor to the specified position
        Args:
            x (integer): the column position
            y (integer): the row position
        """
        self.x = x
        self.y = y
        address = x & 0x3f
        if y & 1:
            address += 0x40 
        if y & 2: 
            address += self.cols
        self.write_cmd(self._DDRAM | address)
    def character(self, char):
        """
            Writes a single character to the display at the current cursor position    
        Args:
            char (string): the character to write
        """
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
        """
            Write a string to the display
        Args:
            string (string): the string to write
        """
        for char in string:
            self.character(char)
    def on(self):
        """
            Turn on the black light
        """
        pass
    def write_cmd(self, cmd):
        """
            Send to command to LCD
        Args:
            cmd (hex): the command to send

        Raises:
            NotImplementedError: NotImplementedError 
        """
        raise NotImplementedError
    def write_data(self, data):
        """
            Send data to LCD
        Args:
            data (hex): the data to send

        Raises:
            NotImplementedError: NotImplementedError
        """
        raise NotImplementedError

MASK_RS = 0x01
MASK_RW = 0x02 
MASK_E  = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA      = 4

class LCD1602(SETUP):
    """
        Class for controlling a 1602 LCD display using the I2C protocol
    Args:
        SETUP (object): inherits from the SETUP class
    """
    def __init__(self, i2c: I2C, address: hex, rows: int, cols: int):
        """
            Initializes the LCD1602 display.
        Args:
            i2c (I2C): object I2C from the machine module (micropython)
            address (hex): address of the LCD display i2c
            rows (integer): set rows the LCD display
            cols (integer): set cols the LCD display
        """
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
        """
            Sends an initialization command to the LCD1602
        Args:
            n (hex): address important with LCD1602
        """
        byte = ((n >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        collect()
    def on(self):
        """
            Turn on black light
        """
        self.i2c.writeto(self.address, bytes([1 << SHIFT_BACKLIGHT]))
        collect()
    def write_cmd(self, cmd):
        """
            Sends a command to the LCD1602
        Args:
            cmd (hex): the command send to the LCD
        """
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
        """
            Sends a data to the LCD1602
        Args:
            data (hex): the data send to the LCD1602
        """
        byte = (MASK_RS | (self.state << SHIFT_BACKLIGHT) | (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        byte = (MASK_RS | (self.state << SHIFT_BACKLIGHT) | ((data & 0x0f) << SHIFT_DATA))      
        self.i2c.writeto(self.address, bytes([byte | MASK_E]))
        self.i2c.writeto(self.address, bytes([byte]))
        collect()