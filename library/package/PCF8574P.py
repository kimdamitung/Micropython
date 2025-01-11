from machine import I2C

class PCF8575:
    _MAX_KEYS = 4
    class Pin:
        def __init__(self, pcf8575, pin):
            self.pcf8575 = pcf8575
            self.pin = pin
        @property
        def value(self):
            return self.pcf8575.OUTPUT(self.pin)
        @value.setter
        def value(self, value):
            self.pcf8575.OUTPUT(self.pin, value)
    def __init__(self, i2c, address = 0x20):
        self.i2c = i2c
        self.address = address
        self.port = bytearray(1)
    def checkDevices(self):
        _address = self.i2c.scan()
        if _address == 0:
            return False
        return [hex(_temp) for _temp in _address]
    @property
    def IO8bit(self):
        self.read()
        return self.port[0]
    @IO8bit.setter
    def IO8bit(self, value):
        self.port[0] = value & 0xFF
        self.write()
    def OUTPUT(self, pin, value=None):
        if not 0 <= pin <= 7:
            raise ValueError(f"Pin {pin} [ERROR 001] not in range 0-7")
        if value is None:
            self.read()
            return (self.port[0] >> pin) & 1
        if value:
            self.port[0] |= 1 << pin
        else:
            self.port[0] &= ~(1 << pin)
        self.write()
    def PIN(self, pin):
        return self.Pin(self, pin)
    def read(self):
        try:
            self.i2c.readfrom_into(self.address, self.port)
        except OSError as e:
            print(e)
    def write(self):
        try:
            self.i2c.writeto(self.address, self.port)
        except OSError as e:
            print(e)
    def setBoard8bit(self, keyboard):
        matrix = [0xFE, 0xFD, 0xFB, 0xF7]
        for i in range(self._MAX_KEYS):
            self.IO8bit = matrix[i]
            value = self.IO8bit
            if value is None:
                return None
            for j in range(self._MAX_KEYS):
                if not (value & (1 << (j + 4))):
                    self.IO8bit = 0xFF
                    return keyboard[j][i]
        self.IO8bit = 0xFF
        return None
    def dictionaries(self, keyboard):
        keys = [
            [keyboard[(i, j)] for j in range(self._MAX_KEYS)]
            for i in range(self._MAX_KEYS)
        ]
        button = self.setBoard16bit(keys)
        return button