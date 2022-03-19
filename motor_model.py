#!/usr/bin/python

from constants import *
from utils import getCounterValues

# 6V 300 Hz
class ActuonixL16R:
    def __init__(self, channel):
        self.freq = 300
        self.maxdc = 60 #
        self.mindc = 30 #
        self.current_state = 0
        self.channel = channel

    def reset(self, pwm):
        on_count, off_count = getCounterValues(delay=0, dc=30)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)
        pwm.setPWMCounters(self.channel, I2C_BUS, on_hex, off_hex)

    def setPWM(self, pwm, channel, dutycycle, delay=0):
        print("Delay: {}, Duty Cycle: {}".format(delay, dutycycle))
        on_count, off_count = getCounterValues(delay, dutycycle)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)

        print("ON: {}, {}, OFF: {}, {}".format(on_count, hex(on_count), off_count, hex(off_count)))
        pwm.setPWMCounters(channel, I2C_BUS, on_hex, off_hex)

# 6V 300 Hz
class ActuonixPQ12R:
    def __init__(self):
        self.freq = 300
        self.maxdc = 30
        self.mindc = 60
        self.current_state = 0

    def reset(self):
        #reset
        return

    def setPWM(self):
        return

# 6 or 12 V 300 Hz
# TODO
class Pololu25D:
    def __init__(self):
        self.freq = 300
        self.current_state = 0

    def reset(self):
        return
    
    def setPWM(self):
        return