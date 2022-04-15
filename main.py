from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
import odroid_wiringpi as wpi
import time
import sys
from PID_controller import PID
from encoder import Encoder
import math

def updatePos(pos):
    print("New position: {}".format(pos))

def main():
    ##################
    # INIT GPIO PINS #
    ##################
    init_gpio()

    ############
    # INIT PWM #
    ############
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
    pwm.setPWMFreq(FREQUENCY)

    ###############
    # INIT MOTORS #
    ###############

    # ACTUATORS
    actuonix_1 = PCA9685(channel=CHANNEL8, freq=300)
    actuonix_1.reset(pwm)
    actuonix_1.setPWM(pwm, dutycycle=30)

    # actuonix_2 = PCA9685(channel=CHANNEL9, freq=300)
    # actuonix_2.reset(pwm)
    # actuonix_2.setPWM(pwm, dutycycle=60)

    # actuonix_3 = PCA9685(channel=CHANNEL10, freq=300)
    # actuonix_3.reset(pwm)
    # actuonix_3.setPWM(pwm, dutycycle=60)

    # actuonix_4 = PCA9685(channel=CHANNEL11, freq=300)
    # actuonix_4.reset(pwm)
    # actuonix_4.setPWM(pwm, dutycycle=60)
    
    # SERVO
    turnigy_1 = PCA9685(channel=CHANNEL12, freq=300)
    turnigy_1.reset(pwm)
    turnigy_1.setPWM(pwm, dutycycle=28)

    # turnigy_2 = PCA9685(channel=CHANNEL13, freq=300)
    # turnigy_2.reset(pwm)
    # turnigy_2.setPWM(pwm, dutycycle=28)
    
    # DC BRUSHED
    pololu_0 = TB9051FTG(channel=CHANNEL0, freq=300, pin_in=MOTORS["pololu_0"]["enc_pins"], pin_out=MOTORS["pololu_0"]["driver_pins"], single=True)
    pololu_0.reset(pwm)

    pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
    pololu_1.reset(pwm)

    # pololu_2 = TB9051FTG(channel=CHANNEL5, freq=300, pin_in=MOTORS["pololu_2"]["enc_pins"], pin_out=MOTORS["pololu_2"]["driver_pins"])
    # pololu_2.reset(pwm)

    # pololu_3 = TB9051FTG(channel=CHANNEL6, freq=300, pin_in=MOTORS["pololu_3"]["enc_pins"], pin_out=MOTORS["pololu_3"]["driver_pins"])
    # pololu_3.reset(pwm)

    # pololu_4 = TB9051FTG(channel=CHANNEL7, freq=300, pin_in=MOTORS["pololu_4"]["enc_pins"], pin_out=MOTORS["pololu_4"]["driver_pins"])
    # pololu_4.reset(pwm)

    # INIT PID CONTROLLERS
    pid_1 = PID(MOTORS["pololu_1"]["enc_pins"], debug=True)
    # pid_2 = PID(MOTORS["pololu_2"]["enc_pins"], debug=True)
    # pid_3 = PID(MOTORS["pololu_3"]["enc_pins"], debug=True)
    # pid_4 = PID(MOTORS["pololu_4"]["enc_pins"], debug=True)

    target = 0
    # target = 1

    buttonA_pressed = False
    buttonB_pressed = False
    buttonX_pressed = False
    buttonY_pressed = False
    joystick_pressed = False

    plate_closed = False

    # TEMP
    wpi.pinMode(27, wpi.INPUT)
    wpi.pullUpDnControl(27, wpi.GPIO.PUD_UP)

    try:
        while True:
            # freq and dc motor testing
            # freq = input("Enter freq: ")
            # dc = input("Enter dc: ")
            # pwm.setPWMFreq(int(freq))
            # pololu_1.forward(pwm, dutycycle=int(dc))
            # pololu_0.forward(pwm, dutycycle=int(dc))

            # A B X Y
            buttonA = wpi.digitalRead(4)   # A
            buttonB = wpi.digitalRead(5)   # B
            buttonX = wpi.digitalRead(6)   # X
            buttonY = wpi.digitalRead(10)  # Y
            
            # Joystick
            js_sw = wpi.digitalRead(27)
            js_vrx = wpi.analogRead(29)
            js_vry = wpi.analogRead(25)

            print(f"SW: {js_sw}, X: {js_vrx}, Y: {js_vry}")

            # ACTUATOR CONTROL
            # target position
            # if target < 30:
            #     if not buttonA:
            #         target += 1
            #         # actuonix_1.setPWM(pwm, dutycycle=target+30)
            #         # time.sleep(0.15)
            # if target > 0:
            #     if not buttonB:
            #         target -= 1
                    # actuonix_1.setPWM(pwm, dutycycle=target+30)
                    # time.sleep(0.15)

            # # SERVO CONTROL
            # while not buttonY:
            #     buttonY_pressed = True
            #     buttonY = wpi.digitalRead(10)  # Y

            # if buttonY_pressed:
            #     if plate_closed:
            #         plate_closed = False
            #         turnigy_1.setPWM(pwm, dutycycle=28)
            #     elif not plate_closed:
            #         plate_closed = True
            #         turnigy_1.setPWM(pwm, dutycycle=51)

            #     buttonY_pressed = False

            # # POLOLU ENCODED
            # if not buttonA:
            #     target += 1
            # if not buttonB:
            #     target -= 1
                
            # # # TODO: create different classes pololu for turnigy & actuators too? to limit range!
            # pid_1.loop(target)

            # # signal the motor
            # if pid_1.getDir() == -1:
            #     pololu_1.forward(pwm, dutycycle=pid_1.getDc())
            # elif pid_1.getDir() == 1:
            #     pololu_1.backward(pwm, dutycycle=pid_1.getDc())

    except KeyboardInterrupt:
        actuonix_1.reset(pwm)
        # actuonix_2.reset(pwm)
        # actuonix_3.reset(pwm)
        # actuonix_4.reset(pwm)
        turnigy_1.reset(pwm)
        # turnigy_2.reset(pwm)
        pololu_0.reset(pwm)
        pololu_1.reset(pwm)
        # pololu_2.reset(pwm)
        # pololu_3.reset(pwm)
        # pololu_4.reset(pwm)
        cleanup()
        sys.exit(0)

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
