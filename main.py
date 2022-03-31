from pwm import PWM
from constants import *
from motor_model import Motor

def main():
    FREQUENCY = 5 # Hz
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS,debug=True)
    pwm.setPWMFreq(FREQUENCY)

    # actuonixL16 = Motor(channel=CHANNEL0, freq=300)
    # actuonixPQ12 = Motor(channel=CHANNEL1, freq=300)

    # actuonixL16.reset(pwm)
    # actuonixPQ12.reset(pwm)

    # actuonixL16.setPWM(pwm, dutycycle=60)
    # actuonixPQ12.setPWM(pwm, dutycycle=30)

    pololu = Motor(channel=CHANNEL2, freq=FREQUENCY)
    pololu.reset(pwm)
    pololu.setPWM(pwm, dutycycle=60)


if __name__ == "__main__":
    main()
