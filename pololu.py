# pololu class and encoder?
import odroid_wiringpi as wpi
from constants import *
from motor_specs import MOTORS

def readEncoder():
    # encA = wpi.digitalRead(MOTORS["pololu_1"]["enc_pins"][0])    # encA
    encB = wpi.digitalRead(MOTORS["pololu_1"]["enc_pins"][1])    # encB

    if encB > 0:
        pos = pos + 1
    else:
        pos = pos - 1
    
    