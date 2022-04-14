# pololu class and encoder?
import odroid_wiringpi as wpi
from constants import *
from motor_specs import MOTORS

class Encoder:
    def __init__(self, encA, encB, callback=None):
        self.encA = encA
        self.encB = encB

        self.pos = 0
        self.dir = None

        self.callback = callback

        # ENCODER INTERRUPT
        wpi.wiringPiISR(5, wpi.GPIO.INT_EDGE_RISING, self.readEncoder) #encA

    def readEncoder(self):
        encB = wpi.digitalRead(4)    # encB

        if encB > 0:
            self.pos += 1
        else:
            self.pos -= 1

        if self.callback != None:
            self.callback(self.pos)
    
    def getPos(self):
        return self.pos