#!/usr/bin/python

from constants import *
from utils import getCounterValues
import odroid_wiringpi as wpi

class SingleTB9051FTG:
    # inputs = [encA, encB]
    # outputs = [ENB, PWM1, PWM2]
    def __init__(self, channel, freq, pin_in, pin_out, debug=False):
        self.freq = freq
        self.current_state = 0 #
        self.channel = channel
        self.debug = debug

        # odroid - motor/driver input and output pins
        self.pin_in = pin_in    # encA encB
        self.pin_out = pin_out  # enb pwm1 pwm2

    def reset(self, pwm):
        # reset PCA9685
        if self.debug:
            print("Reseting PCA9685")
        on_count, off_count = getCounterValues(delay=0, dc=0)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)
        pwm.setPWMCounters(self.channel, I2C_BUS, on_hex, off_hex)  # EN = 0

        # reset TB9051FTG
        if self.debug:
            print("Reseting TB9051FTG")

        # setup wpi
        wpi.wiringPiSetup()
        # set pin mode
        for pin in self.pin_in:
            wpi.pinMode(pin, IN)
        for pin in self.pin_out:
            wpi.pinMode(pin, OUT)
        # init pins
        wpi.digitalWrite(self.pin_out[0], 0)    # ENB = 0
        wpi.digitalWrite(self.pin_out[1], 0)    # PWM1 = 0
        wpi.digitalWrite(self.pin_out[2], 0)    # PWM2 = 0

    def forward(self, pwm, dutycycle):
        wpi.digitalWrite(self.pin_out[0], 0)    # ENB = 0
        wpi.digitalWrite(self.pin_out[1], 1)    # PWM1 = 1
        wpi.digitalWrite(self.pin_out[2], 0)    # PWM2 = 0

        self.setPWM(pwm, dutycycle)
    
    def backward(self, pwm, dutycycle):
        wpi.digitalWrite(self.pin_out[0], 0)    # ENB = 0
        wpi.digitalWrite(self.pin_out[1], 0)    # PWM1 = 0
        wpi.digitalWrite(self.pin_out[2], 1)    # PWM2 = 1

        self.setPWM(pwm, dutycycle)
    
    def stop(self, pwm):
        wpi.digitalWrite(self.pin_out[0], 0)    # ENB = 0
        wpi.digitalWrite(self.pin_out[1], 0)    # PWM1 = 0
        wpi.digitalWrite(self.pin_out[2], 0)    # PWM2 = 0

        self.setPWM(pwm, 0)

    def setPWM(self, pwm, dutycycle, delay=0):
        print("Delay: {}, Duty Cycle: {}".format(delay, dutycycle))
        on_count, off_count = getCounterValues(delay, dutycycle)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)

        print("ON: {}, {}, OFF: {}, {}".format(on_count, hex(on_count), off_count, hex(off_count)))
        pwm.setPWMCounters(self.channel, I2C_BUS, on_hex, off_hex)


