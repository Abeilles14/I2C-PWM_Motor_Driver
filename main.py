from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
import odroid_wiringpi as wpi
import time
import sys
from PID_controller import PID
import math

def updatePos(pos):
    print("New position: {}".format(pos))

def main():
    # INIT GPIO PINS
    init_gpio()

    # SET PWM FREQ
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
    pwm.setPWMFreq(FREQUENCY)

    # INIT MOTORS
    actuonix_1 = PCA9685(channel=CHANNEL8, freq=300)
    actuonix_1.reset(pwm)
    actuonix_1.setPWM(pwm, dutycycle=30)
    
    turnigy_1 = PCA9685(channel=CHANNEL12, freq=300)
    turnigy_1.reset(pwm)
    turnigy_1.setPWM(pwm, dutycycle=28)
    
    pololu_0 = TB9051FTG(channel=CHANNEL0, freq=300, pin_in=MOTORS["pololu_0"]["enc_pins"], pin_out=MOTORS["pololu_0"]["driver_pins"], single=True)
    pololu_0.reset(pwm)

    pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
    pololu_1.reset(pwm)

    # INIT PID CONTROLLERS
    pid_1 = PID(debug=True)

    # target = 0
    target = 1

    try:
        while True:
            # freq and dc motor testing
            # freq = input("Enter freq: ")
            # dc = input("Enter dc: ")
            # pwm.setPWMFreq(int(freq))
            # pololu_1.forward(pwm, dutycycle=int(dc))
            # pololu_0.forward(pwm, dutycycle=int(dc))

            button1 = wpi.digitalRead(15)
            button2 = wpi.digitalRead(16)
            
            # target position
            if target < 30:
                if not button1:
                    target += 1
                    actuonix_1.setPWM(pwm, dutycycle=target+30)
                    time.sleep(0.15)
            if target > 0:
                if not button2:
                    target -= 1
                    actuonix_1.setPWM(pwm, dutycycle=target+30)
                    time.sleep(0.15)
                
            print(target)

            # # TODO: Possibly put this in a pololu motor class? 
            # # TODO: create different classes for turnigy & actuators too? to limit range!
            # pid_1.loop(target)

            # # signal the motor
            # if pid_1.getDir() == -1:
            #     pololu_1.forward(pwm, dutycycle=pid_1.getDc())
            # elif pid_1.getDir() == 1:
            #     pololu_1.backward(pwm, dutycycle=pid_1.getDc())

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

    for pin in GPIO_OUT:
        wpi.pinMode(pin, wpi.OUTPUT)
        # init out pins low
        wpi.digitalWrite(pin, 0)

def cleanup():
    # unexport pins
    for pin in range(0, 256):
        file = open("/sys/class/gpio/unexport","w")
        file.write(str(pin))


if __name__ == "__main__":
    main()
