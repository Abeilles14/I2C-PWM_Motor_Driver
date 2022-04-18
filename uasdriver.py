import time
import sys
import mecanum
import math
import logging as log
import odroid_wiringpi as wpi
from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
from utils import remap_range
from PID_controller import PID
from encoder import Encoder

log.basicConfig(level=log.DEBUG)

class UASDriver:
    def __init__(self):
        log.info("Starting Motor Drive System init...")

        ############################
        # INIT MOTOR TARGET VALUES #
        ############################
        self.target_pololu = [0, 0, 0, 0, 0] # p0, p1, p2, p3, p4 = [w, fl, fr, rl, rr]
        self.target_actuator = [0, 0]  # a1, a2, a3, a4 = [vertical, horizontal]
        self.target_turnigy = [0] #t1, t2 = [in/out]

        self.plate_closed = False
        self.ljs_pressed = False
        self.mode = ControlMode.IDLE

        ######################
        # INIT REMOTE VALUES #
        ######################
        self.buttonA = 1
        self.buttonB = 1
        self.buttonX = 1
        self.buttonY = 1

        self.ljs_x = 0.0
        self.ljs_y = 0.0
        self.ljs_sw = 1
        self.rjs_x = 0.0
        self.rjs_y = 0.0
        self.rjs_sw = 1

        ##################
        # INIT GPIO PINS #
        ##################
        self.init_gpio()

        ############
        # INIT PWM #
        ############
        log.debug("Init PWM...")
        self.pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
        self.pwm.setPWMFreq(FREQUENCY)

        ###############
        # INIT MOTORS #
        ###############
        log.debug("Init Motors...")
        # ACTUATORS
        self.actuonix_1 = PCA9685(channel=CHANNEL8, freq=300)
        self.actuonix_1.reset(self.pwm)
        self.actuonix_1.setPWM(self.pwm, dutycycle=30)

        self.actuonix_2 = PCA9685(channel=CHANNEL9, freq=300)
        self.actuonix_2.reset(self.pwm)
        self.actuonix_2.setPWM(self.pwm, dutycycle=30)

        self.actuonix_3 = PCA9685(channel=CHANNEL10, freq=300)
        self.actuonix_3.reset(self.pwm)
        self.actuonix_3.setPWM(self.pwm, dutycycle=30)

        self.actuonix_4 = PCA9685(channel=CHANNEL11, freq=300)
        self.actuonix_4.reset(self.pwm)
        self.actuonix_4.setPWM(self.pwm, dutycycle=30)
        
        # SERVO
        self.turnigy_1 = PCA9685(channel=CHANNEL12, freq=300)
        self.turnigy_1.reset(self.pwm)
        self.turnigy_1.setPWM(self.pwm, dutycycle=28)

        self.turnigy_2 = PCA9685(channel=CHANNEL13, freq=300)
        self.turnigy_2.reset(self.pwm)
        self.turnigy_2.setPWM(self.pwm, dutycycle=28)
        
        # DC BRUSHED
        self.pololu_0 = TB9051FTG(channel=CHANNEL0, freq=300, pin_in=MOTORS["pololu_0"]["enc_pins"], pin_out=MOTORS["pololu_0"]["driver_pins"], single=True)
        self.pololu_0.reset(self.pwm)

        self.pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
        self.pololu_1.reset(self.pwm)

        self.pololu_2 = TB9051FTG(channel=CHANNEL5, freq=300, pin_in=MOTORS["pololu_2"]["enc_pins"], pin_out=MOTORS["pololu_2"]["driver_pins"])
        self.pololu_2.reset(self.pwm)

        self.pololu_3 = TB9051FTG(channel=CHANNEL6, freq=300, pin_in=MOTORS["pololu_3"]["enc_pins"], pin_out=MOTORS["pololu_3"]["driver_pins"])
        self.pololu_3.reset(self.pwm)

        self.pololu_4 = TB9051FTG(channel=CHANNEL7, freq=300, pin_in=MOTORS["pololu_4"]["enc_pins"], pin_out=MOTORS["pololu_4"]["driver_pins"])
        self.pololu_4.reset(self.pwm)

        # INIT PID CONTROLLERS
        log.debug("Init PID controllers...")
        self.pid_1 = PID(MOTORS["pololu_1"]["enc_pins"])
        self.pid_2 = PID(MOTORS["pololu_2"]["enc_pins"])
        self.pid_3 = PID(MOTORS["pololu_3"]["enc_pins"])
        self.pid_4 = PID(MOTORS["pololu_4"]["enc_pins"])

        log.info("Motor Drive System init complete! Starting main routine...")
        self.controlLoop()
    
    def setRemoteValues(self, buttonA, buttonB, buttonX, buttonY, ljs_x, ljs_y, ljs_sw, rjs_x, rjs_y, rjs_sw):
        # joystick movement tolerance
        if ljs_x < 0.2 and ljs_x > -0.2:
            ljs_x = 0.0
        if ljs_y < 0.2 and ljs_y > -0.2:
            ljs_y = 0.0
        if rjs_x < 0.2 and rjs_x > -0.2:
            rjs_x = 0.0

        self.buttonA = buttonA
        self.buttonB = buttonB
        self.buttonX = buttonX
        self.buttonY = buttonY

        self.ljs_x = ljs_x
        self.ljs_y = ljs_y
        self.ljs_sw = ljs_sw
        self.rjs_x = rjs_x
        self.rjs_y = rjs_y
        self.rjs_sw = rjs_sw

        log.debug(f"lSW: {ljs_sw}, lX: {ljs_x}, lY: {ljs_y}, rX: {rjs_x}")
    
    def updatePosCallback(self, pos):
        log.info("New position: {}".format(pos))

    def controlLoop(self):

        try:
            while True:
                # NOTE: remote control values are set in the main thread

                # button debouncing detection
                while not self.buttonA:
                    self.button_pressed = [1, 0, 0, 0]
                    log.info("DRIVE MODE")
                while not self.buttonB:
                    self.button_pressed = [0, 1, 0, 0]
                    log.info("WINCH MODE")
                while not self.buttonX:
                    self.button_pressed = [0, 0, 1, 0]
                    log.info("CLAW MODE")
                while not self.buttonY:
                    self.button_pressed = [0, 0, 0, 1]
                    log.info("IDLE MODE")
                while not self.ljs_sw:
                    self.ljs_pressed = True

                # mode assignment
                if self.button_pressed[0]:
                    self.mode = ControlMode.DRIVE
                elif self.button_pressed[1]:
                    self.mode = ControlMode.WINCH
                elif self.button_pressed[2]:
                    self.mode = ControlMode.CLAW
                elif self.button_pressed[3]:
                    self.mode = ControlMode.IDLE
                else:
                    log.error("ERROR: mode not recognized :(")

                # move according to mode and joystick ctrls
                if self.mode == ControlMode.IDLE:
                    log.debug("idle")
                    pass

                elif self.mode == ControlMode.DRIVE:
                    log.debug("drive")

                    self.target_pololu = mecanum.setMotorTargets(self.ljs_x, self.ljs_y, self.rjs_x, self.target_pololu)

                    log.debug(f"target: {self.target_pololu}")
                    log.debug(f"pos: {[0.0, self.pid_1.getDc(), self.pid_2.getDc(), self.pid_3.getDc(), self.pid_4.getDc()]}")

                    self.pid_1.loop(round(self.target_pololu[1]))
                    self.pid_2.loop(round(self.target_pololu[2]))
                    self.pid_3.loop(round(self.target_pololu[3]))
                    self.pid_4.loop(round(self.target_pololu[4]))

                    # signal the motors
                    if self.pid_1.getDir() == -1:
                        self.pololu_1.forward(self.pwm, dutycycle=self.pid_1.getDc())
                    elif self.pid_1.getDir() == 1:
                        self.pololu_1.backward(self.pwm, dutycycle=self.pid_1.getDc())
                    
                    if self.pid_2.getDir() == -1:
                        self.pololu_2.forward(self.pwm, dutycycle=self.pid_2.getDc())
                    elif self.pid_2.getDir() == 1:
                        self.pololu_2.backward(self.pwm, dutycycle=self.pid_2.getDc())

                    if self.pid_3.getDir() == -1:
                        self.pololu_3.forward(self.pwm, dutycycle=self.pid_3.getDc())
                    elif self.pid_3.getDir() == 1:
                        self.pololu_3.backward(self.pwm, dutycycle=self.pid_3.getDc())

                    if self.pid_4.getDir() == -1:
                        self.pololu_4.forward(self.pwm, dutycycle=self.pid_4.getDc())
                    elif self.pid_4.getDir() == 1:
                        self.pololu_4.backward(self.pwm, dutycycle=self.pid_4.getDc())
                
                elif self.mode == ControlMode.WINCH:
                    log.debug("winch")
                    if self.ljs_y > 0.3:
                        self.pololu_0.forward(self.pwm, dutycycle=WINCH_DC_SPEED)
                    elif self.ljs_y < -0.3:
                        self.pololu_0.backward(self.pwm, dutycycle=WINCH_DC_SPEED)
                    else:
                        self.pololu_0.backward(self.pwm, dutycycle=0)

                elif self.mode == ControlMode.CLAW:
                    log.debug("claw")

                    # VERTICAL ACTUATORS
                    log.debug(f"DC1: {self.target_actuator[0]}, DC2: {self.target_actuator[1]}")

                    # not allowed: 30 & y+, 0 and y-
                    if not ((math.ceil(self.target_actuator[0]) >= 30 and self.ljs_y > -0.2) or (math.floor(self.target_actuator[0]) == 0 and self.ljs_y < 0.2)):
                        self.target_actuator[0] += self.ljs_y
                        self.actuonix_1.setPWM(self.pwm, dutycycle=self.target_actuator[0]+30)
                        self.actuonix_2.setPWM(self.pwm, dutycycle=self.target_actuator[0]+30)
                        time.sleep(0.08)

                    # HORIZONTAL ACTUATORS
                    # not allowed: 30 & y+, 0 and y-
                    if not ((math.ceil(self.target_actuator[1]) >= 30 and self.ljs_x > -0.2) or (math.floor(self.target_actuator[1]) == 0 and self.ljs_x < 0.2)):
                        self.target_actuator[1] += self.ljs_x
                        self.actuonix_3.setPWM(self.pwm, dutycycle=self.target_actuator[1]+ACTUATOR_DC_MIN)
                        self.actuonix_4.setPWM(self.pwm, dutycycle=self.target_actuator[1]+ACTUATOR_DC_MIN)
                        time.sleep(0.08)

                    if self.ljs_pressed:
                        if plate_closed:
                            plate_closed = False
                            self.turnigy_1.setPWM(self.pwm, dutycycle=28)
                            self.turnigy_2.setPWM(self.pwm, dutycycle=28)
                        elif not plate_closed:
                            plate_closed = True
                            self.turnigy_1.setPWM(self.pwm, dutycycle=56)
                            self.turnigy_2.setPWM(self.pwm, dutycycle=56)

                        self.ljs_pressed = False
                else:
                    log.error("Mode not recognized :(")

        except KeyboardInterrupt:
            self.cleanup()
            sys.exit(0)

    def init_gpio(self):
        log.info("Init GPIO...")
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
        log.info("Init GPIO complete!")

    def cleanup(self):
        log.info("Cleaning up driver system...")
        # reset motors
        self.actuonix_1.reset(self.pwm)
        self.actuonix_2.reset(self.pwm)
        self.actuonix_3.reset(self.pwm)
        self.actuonix_4.reset(self.pwm)
        self.turnigy_1.reset(self.pwm)
        self.turnigy_2.reset(self.pwm)
        self.pololu_0.reset(self.pwm)
        self.pololu_1.reset(self.pwm)
        self.pololu_2.reset(self.pwm)
        self.pololu_3.reset(self.pwm)
        self.pololu_4.reset(self.pwm)
        
        # unexport pins
        for pin in range(0, 256):
            file = open("/sys/class/gpio/unexport","w")
            file.write(str(pin))

        log.info("Driver system cleanup complete!")