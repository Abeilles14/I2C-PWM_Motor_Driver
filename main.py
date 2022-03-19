from pwm import PWM
from constants import *
from motor_model import Motor, ActuonixL16R, Pololu25D

def main():
    FREQUENCY = 300 # Hz
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS,debug=True)
    pwm.setPWMFreq(FREQUENCY)
    

    actuonix0 = Motor(channel=0, freq=300)
    actuonix0.reset()
    actuonix0.setPWM(pwm, channel=0, dutycycle=60)

if __name__ == "__main__":
    main()
