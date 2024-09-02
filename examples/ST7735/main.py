import esp
esp.osdebug(0)
#import module micropython
from package.display.TFT.ST7735 import ST7735, Font_11x18
from package.display.TFT import images
from machine import SPI, Pin

spi = SPI(1, baudrate = 20000000, polarity = 0, phase = 0, sck = Pin(12), mosi = Pin(11), miso = None)
st7735 = ST7735(spi, cs = Pin(15, Pin.OUT), dc = Pin(16, Pin.OUT), reset = Pin(17, Pin.OUT))
st7735.init()
st7735.setScreen(st7735._COLOR565(0xFF, 0xFF, 0xFF))
st7735.setImagesFullScreen(images)
while True:
    '''code'''
    pass