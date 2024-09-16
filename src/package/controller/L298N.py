from  machine import Pin, PWM
from utime import sleep_us

class L298N(object):
    def __init__(self, in1: int, in2: int, in3: int , in4: int, enA: int = None, enB: int = None, frequency = 1000):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.in3 = Pin(in3, Pin.OUT)
        self.in4 = Pin(in4, Pin.OUT)
        self.enA = None
        self.enB = None
        if enA is not None and enB is not None:
            self.enA = PWM(Pin(enA), freq=frequency)
            self.enB = PWM(Pin(enB), freq=frequency)
    def stop(self):
        if self.enA is not None:
            self.enA.duty(0)
        self.in1.value(0)
        self.in2.value(0)
        if self.enB is not None:
            self.enB.duty(0)
        self.in3.value(0)
        self.in4.value(0)
        sleep_us(1)
    def forward(self, speed: int):
        if 0 < speed <= 100:
            if self.enA is not None:
                self.enA.duty(int(speed * 1023 / 100))
            self.in1.value(1)
            self.in2.value(0)
            if self.enB is not None:
                self.enB.duty(int(speed * 1023 / 100))
            self.in3.value(1)
            self.in4.value(0)
        sleep_us(1)
    def backward(self, speed: int):
        if 0 < speed <= 100:
            if self.enA is not None:
                self.enA.duty(int(speed * 1023 / 100))
            self.in1.value(0)
            self.in2.value(1)
            if self.enB is not None:
                self.enB.duty(int(speed * 1023 / 100))
            self.in3.value(0)
            self.in4.value(1)
        sleep_us(1)
    def right(self, speed: int):
        if 0 < speed <= 100:
            if self.enA is not None:
                self.enA.duty(int(speed * 1023 / 100))
            self.in1.value(1)
            self.in2.value(0)
            if self.enB is not None:
                self.enB.duty(int(speed * 1023 / 100))
            self.in3.value(0)
            self.in4.value(1)
        sleep_us(1)
    def left(self, speed: int):
        if 0 < speed <= 100:
            if self.enA is not None:
                self.enA.duty(int(speed * 1023 / 100))
            self.in1.value(0)
            self.in2.value(1)
            if self.enB is not None:
                self.enB.duty(int(speed * 1023 / 100))
            self.in3.value(1)
            self.in4.value(0)
        sleep_us(1)