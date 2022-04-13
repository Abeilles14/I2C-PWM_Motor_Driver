from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
import odroid_wiringpi as wpi

def main():
    init_gpio()
    
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS,debug=True)
    FREQUENCY=300
    pwm.setPWMFreq(FREQUENCY)

    actuonix_1 = PCA9685(channel=CHANNEL0, freq=300)
    actuonix_1.reset(pwm)
    
    turnigy_1 = PCA9685(channel=CHANNEL12, freq=300)
    turnigy_1.reset(pwm)
    
    pololu_0 = TB9051FTG(channel=CHANNEL0, freq=300, pin_in=MOTORS["pololu_0"]["enc_pins"], pin_out=MOTORS["pololu_0"]["driver_pins"], single=True)
    pololu_0.reset(pwm)

    pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
    pololu_1.reset(pwm)

    while True:
        motor = input("Enter p for pololu, a for actuator, t for turnigy: ")
        if motor == "p":
            freq = input("Enter frequency: ")
            pwm.setPWMFreq(int(freq))

            direction = input("Enter f for fwd, b for bkwd, s for stop: ")

            if direction == "f":
                print("Going forward")
                pololu_1.forward(pwm, dutycycle=60)
            elif direction == "b":
                print("Going Backward")
                pololu_1.backward(pwm, dutycycle=60)
            elif direction == "s":
                print("Stopping")
                pololu_1.stop(pwm)
        elif motor == "a":
            direction = input("Enter o for out, i for in: ")

            if direction == "i":
                print("Going in")
                actuonix_1.setPWM(pwm, dutycycle=30)
            elif direction == "o":
                print("Going out")
                actuonix_1.setPWM(pwm, dutycycle=60)
        elif motor == "t":
            direction = input("Enter f for fwd, b for bkwd: ")

            if direction == "f":
                print("Going forward")
                turnigy_1.setPWM(pwm, dutycycle=28)
            elif direction == "b":
                print("Going Backward")
                turnigy_1.setPWM(pwm, dutycycle=64)

def init_gpio():
    # setup wpi
    wpi.wiringPiSetup()
    
    # set pin mode
    for pin in GPIO_IN:
        wpi.pinMode(pin, IN)

    for pin in GPIO_OUT:
        wpi.pinMode(pin, OUT)

        # init out pins low
        wpi.digitalWrite(pin, 0)


if __name__ == "__main__":
    main()
