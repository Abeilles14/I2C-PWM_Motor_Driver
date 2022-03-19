from pwm import PWM
from constants import *
from motor_model import ActuonixL16R, Pololu25D

def main():
    FREQUENCY = 300 # Hz
    DELAY = 10 # percent
    DUTYCYCLE = 30 # percent

    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS,debug=True)
    pwm.setPWMFreq(FREQUENCY)
    
    actuator1 = ActuonixL16R()

if __name__ == "__main__":
    main()