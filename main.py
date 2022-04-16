from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
from utils import remap_range
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
    pid_1 = PID(MOTORS["pololu_1"]["enc_pins"])
    # pid_2 = PID(MOTORS["pololu_2"]["enc_pins"], debug=True)
    # pid_3 = PID(MOTORS["pololu_3"]["enc_pins"], debug=True)
    # pid_4 = PID(MOTORS["pololu_4"]["enc_pins"], debug=True)

    # TODO: Remove, TEMP joystick button
    button_pressed = [0, 0, 0, 1]    # A B X Y
    joystick_pressed = False

    wpi.pinMode(27, wpi.INPUT)
    wpi.pullUpDnControl(27, wpi.GPIO.PUD_UP)
    ################

    target_pololu = [0, 0, 0, 0, 0] # p0, p1, p2, p3, p4 = [w, fl, fr, rl, rr]
    target_actuator = [0, 0]  # a1, a2, a3, a4 = [vertical, horizontal]
    target_turnigy = [0] #t1, t2 = [in/out]

    plate_closed = False
    mode = ControlMode.IDLE

    try:
        while True:
            # freq and dc motor testing
            # freq = input("Enter freq: ")
            # dc = input("Enter dc: ")
            # pwm.setPWMFreq(int(freq))
            # pololu_1.forward(pwm, dutycycle=int(dc))
            # pololu_0.forward(pwm, dutycycle=int(dc))

            # TODO: Remove, Temp code for joystick
            # A B X Y
            buttonA = wpi.digitalRead(4)   # A
            buttonB = wpi.digitalRead(5)   # B
            buttonX = wpi.digitalRead(10)   # X
            buttonY = wpi.digitalRead(6)  # Y

            # button debouncing detection
            while not buttonA:
                button_pressed = [1, 0, 0, 0]
                buttonA = wpi.digitalRead(4)
                print("DRIVE MODE")
            while not buttonB:
                button_pressed = [0, 1, 0, 0]
                buttonB = wpi.digitalRead(5)
                print("WINCH MODE")
            while not buttonX:
                button_pressed = [0, 0, 1, 0]
                buttonX = wpi.digitalRead(10)
                print("CLAW MODE")
            while not buttonY:
                button_pressed = [0, 0, 0, 1]
                buttonY = wpi.digitalRead(6)
                print("IDLE MODE")

            # mode assignment
            if button_pressed[0]:
                mode = ControlMode.DRIVE
            elif button_pressed[1]:
                mode = ControlMode.WINCH
            elif button_pressed[2]:
                mode = ControlMode.CLAW
            elif button_pressed[3]:
                mode = ControlMode.IDLE
            else:
                print("ERROR: mode not recognized :(")

            # TODO: Remove once xbox remote connected
            # joystick detection
            js_sw = wpi.digitalRead(27)
            js_vrx = wpi.analogRead(25)
            js_vry = wpi.analogRead(29)

            sc_vrx, sc_vry= remap_range(js_vrx, js_vry)

            if sc_vry < 0.05 and sc_vry > -0.05:
                sc_vry = 0.0
            if sc_vrx < 0.05 and sc_vrx > -0.05:
                sc_vrx = 0.0

            print(f"SW: {js_sw}, sX: {sc_vrx}, sY: {sc_vry}")
            ################################

            # move according to mode and joystick ctrls
            if mode == ControlMode.IDLE:
                print("idle")
                pass

            elif mode == ControlMode.DRIVE:
                print("drive")
                # TODO: add more controls for all wheels and mecanum
                pass
                # if sc_vry > 0:
                #     target += sc_vry
                # elif sc_vry < 0:
                #     target -= sc_vry
                    
                # # # TODO: create different classes pololu for turnigy & actuators too? to limit range!
                # pid_1.loop(round(target))

                # # signal the motor
                # if pid_1.getDir() == -1:
                #     pololu_1.forward(pwm, dutycycle=pid_1.getDc())
                # elif pid_1.getDir() == 1:
                #     pololu_1.backward(pwm, dutycycle=pid_1.getDc())
            
            elif mode == ControlMode.WINCH:
                print("winch")
                if sc_vry > 0.5:
                    pololu_0.forward(pwm, dutycycle=60)
                elif sc_vry < 0.5:
                    pololu_0.backward(pwm, dutycycle=60)

            elif mode == ControlMode.CLAW:
                print("claw")

                # VERTICAL ACTUATORS
                print(f"DC: {target_actuator[0]}")

                # not allowed: 30 & y+, 0 and y-
                if not ((math.ceil(target_actuator[0]) >= 30 and sc_vry > 0.1) or (math.floor(target_actuator[0]) == 0 and sc_vry < 0.1)):
                    target_actuator[0] += sc_vry
                    actuonix_1.setPWM(pwm, dutycycle=target_actuator[0]+30)
                    # actuonix_2.setPWM(pwm, dutycycle=target_actuator[0]+30)
                    time.sleep(0.08)
                

                # HORIZONTAL ACTUATORS
                # not allowed: 30 & y+, 0 and y-
                if not ((math.ceil(target_actuator[1]) >= 30 and sc_vrx > 0.1) or (math.floor(target_actuator[1]) == 0 and sc_vrx < 0.1)):
                    target_actuator[1] += sc_vrx
                    # actuonix_3.setPWM(pwm, dutycycle=target_actuator[1]+30)
                    # actuonix_4.setPWM(pwm, dutycycle=target_actuator[1]+30)
                    time.sleep(0.08)

                # JOYSTICK SWITCH
                while not js_sw:
                    joystick_pressed = True
                    js_sw = wpi.digitalRead(27)

                if joystick_pressed:
                    if plate_closed:
                        plate_closed = False
                        turnigy_1.setPWM(pwm, dutycycle=28)
                        # turnigy_2.setPWM(pwm, dutycycle=28)
                    elif not plate_closed:
                        plate_closed = True
                        turnigy_1.setPWM(pwm, dutycycle=51)
                        # turnigy_2.setPWM(pwm, dutycycle=51)

                    joystick_pressed = False


            else:
                print("ERROR: mode not recognized :(")


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
