from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
import odroid_wiringpi as wpi
import time
import sys
from encoder import Encoder
from utils import pwmToDc
import math
# import matplotlib.pyplot as plt

def updatePos(pos):
    print("New position: {}".format(pos))

def main():
    # init pins
    init_gpio()

    # set pwm frequency
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
    pwm.setPWMFreq(FREQUENCY)

    actuonix_1 = PCA9685(channel=CHANNEL8, freq=300)
    actuonix_1.reset(pwm)
    
    turnigy_1 = PCA9685(channel=CHANNEL12, freq=300)
    turnigy_1.reset(pwm)
    
    pololu_0 = TB9051FTG(channel=CHANNEL0, freq=300, pin_in=MOTORS["pololu_0"]["enc_pins"], pin_out=MOTORS["pololu_0"]["driver_pins"], single=True)
    pololu_0.reset(pwm)

    pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
    pololu_1.reset(pwm)

    enc1 = Encoder(4, 5) # callback = updatePos

    pos = 0
    prevT = float(0)
    eprev = float(0)
    eintegral = float(0)

    try:
        while True:
            # freq and dc motor testing
            # freq = input("Enter freq: ")
            # dc = input("Enter dc: ")
            # pwm.setPWMFreq(int(freq))
            # pololu_1.forward(pwm, dutycycle=int(dc))
            # pololu_0.forward(pwm, dutycycle=int(dc))

            # current time
            sec = time.time()

            # current pos
            pos = enc1.getPos()

            # target position
            target = 500
            # target = 250*math.sin(prevT);

            # PID constants
            kp = float(1.0)
            kd = float(0.0)
            ki = float(0.0)

            # time difference
            currT = time.time()
            deltaT = float(currT - prevT)
            prevT = currT

            # error
            e = pos - target

            # derivative
            dedt = (e - eprev)/(deltaT)

            # integral
            eintegral = eintegral + e*deltaT

            # control signal
            u = float(kp*e + kd*dedt + ki*eintegral)

            # motor power
            pwr = float(abs(u))
            if pwr > 255:
                pwr = 255
            
            dc = pwmToDc(pwr)
            if dc > 99:
                dc = 99
            elif dc < 10:
                dc = 0
            
            # motor direction
            dir = 1
            if u < 0:
                dir = -1

            # signal the motor
            if dir == -1:
                pololu_1.forward(pwm, dutycycle=dc)
                # pololu_0.forward(pwm, dutycycle=dc)
            elif dir == 1:
                pololu_1.backward(pwm, dutycycle=dc)
                # pololu_0.backward(pwm, dutycycle=dc)

            # store previous error
            eprev = e

            # plt.axis([0, 10, 0, 1])
            # y = pos
            # x = sec
            # plt.scatter(x, y)
            # plt.pause(0.05)

            print(f"target: {target} pos: {enc1.getPos()}, pwr: {pwr}, dc: {dc}, e: {e}")


    except KeyboardInterrupt:
        pololu_1.reset(pwm)
        pololu_0.reset(pwm)
        cleanup()
        sys.exit(0)

    # while True:
    #     motor = input("Enter p0 for pololu0, p1 for pololu1, a for actuator, t for turnigy: ")
    #     if motor == "p0":
    #         direction = input("Enter f for fwd, b for bkwd, s for stop: ")

    #         if direction == "f":
    #             print("Going forward")
    #             pololu_0.forward(pwm, dutycycle=60)
    #         elif direction == "b":
    #             print("Going Backward")
    #             pololu_0.backward(pwm, dutycycle=60)
    #         elif direction == "s":
    #             print("Stopping")
    #             pololu_0.stop(pwm)
    #     elif motor == "p1":
    #         direction = input("Enter f for fwd, b for bkwd, s for stop: ")

    #         if direction == "f":
    #             print("Going forward")
    #             pololu_1.forward(pwm, dutycycle=60)
    #         elif direction == "b":
    #             print("Going Backward")
    #             pololu_1.backward(pwm, dutycycle=60)
    #         elif direction == "s":
    #             print("Stopping")
    #             pololu_1.stop(pwm)
    #     elif motor == "a":
    #         direction = input("Enter o for out, i for in: ")

    #         if direction == "i":
    #             print("Going in")
    #             actuonix_1.setPWM(pwm, dutycycle=30)
    #         elif direction == "o":
    #             print("Going out")
    #             actuonix_1.setPWM(pwm, dutycycle=60)
    #     elif motor == "t":
    #         direction = input("Enter f for fwd, b for bkwd: ")

    #         if direction == "f":
    #             print("Going forward")
    #             turnigy_1.setPWM(pwm, dutycycle=28)
    #         elif direction == "b":
    #             print("Going Backward")
    #             turnigy_1.setPWM(pwm, dutycycle=64)

def init_gpio():
    # unexport pins
    for pin in range(0, 256):
        file = open("/sys/class/gpio/unexport","w")
        file.write(str(pin))

    # setup wpi
    wpi.wiringPiSetup()
    
    # set pin mode
    for pin in GPIO_IN:
        wpi.pinMode(pin, wpi.INPUT)
        wpi.pullUpDnControl(pin, wpi.GPIO.PUD_UP)

    # for pin in GPIO_OUT:
    #     wpi.pinMode(pin, OUT)

        # init out pins low
        # wpi.digitalWrite(pin, 0)

def cleanup():
    # unexport pins
    for pin in range(0, 256):
        file = open("/sys/class/gpio/unexport","w")
        file.write(str(pin))


if __name__ == "__main__":
    main()
