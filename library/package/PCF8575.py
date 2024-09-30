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
        self.port = bytearray(2)
    def checkDevices(self):
        _address = self.i2c.scan()
        if _address == 0:
            return False
        return [hex(_temp) for _temp in _address]
    @property
    def IO16bit(self):
        self.read()
        return self.port[0] | (self.port[1] << 8)
    @IO16bit.setter
    def IO16bit(self, value):
        self.port[0] = value & 0xFF
        self.port[1] = (value >> 8) & 0xFF
        self.write()
    def OUTPUT(self, pin, value = None):
        if not 0 <= pin <= 7 and not 10 <= pin <= 17:
            raise ValueError(f"Pin {pin} [ERROR 001] not 16 bit 0 - 7 and 10 - 17")
        if pin >= 10:
            pin -= 2
        if value is None:
            self.read()
            return (self.port[pin // 8] >> (pin % 8)) & 1
        if value:
            self.port[pin // 8] |= 1 << (pin % 8)
        else:
            self.port[pin // 8] &= ~(1 << (pin % 8))
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
    def setBoard16bit(self, keyboard):
        matrix = [0xFFFE, 0xFFFD, 0xFFFB, 0xFFF7]
        for i in range(self._MAX_KEYS):
            self.IO16bit = matrix[i]
            value = self.IO16bit
            if value is None:
                return None
            for j in range(self._MAX_KEYS):
                if not (value & (1 << (j + 4))):
                    self.IO16bit = 0xFFFF
                    return keyboard[j][i]
        self.IO16bit = 0xFFFF
        return None
    def dictionaries(self, keyboard):
        keys = [
            [keyboard[(i, j)] for j in range(self._MAX_KEYS)]
            for i in range(self._MAX_KEYS)
        ]
        button = self.setBoard16bit(keys)
        return button