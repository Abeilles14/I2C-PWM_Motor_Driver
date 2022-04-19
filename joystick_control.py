import time
import sys
import mecanum
import math
import logging
import odroid_wiringpi as wpi
from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
from utils import remap_range
from PID_controller import PID
from encoder import Encoder

logging.getLogger("Adafruit_I2C.Device.Bus.{0}.Address.{1:#0X}".format(0, 0X40)).setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
uaslog = logging.getLogger("UASlogger")

PIN_A = 27
PIN_B = 23
PIN_X = 26
PIN_Y = 10

PIN_LJSX = 25
PIN_LJSY = 29
        
class JoystickControl:
    def __init__(self):
        ############################
        # INIT MOTOR TARGET VALUES #
        ############################
        self.target_pololu = [0, 0, 0, 0, 0] # p0, p1, p2, p3, p4 = [w, fl, fr, rl, rr]

        ######################
        # INIT REMOTE VALUES #
        ######################
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
        uaslog.debug("Init PWM...")
        self.pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
        self.pwm.setPWMFreq(FREQUENCY)

        ###############
        # INIT MOTORS #
        ###############
        uaslog.debug("Init Motors...")
        # DC BRUSHED
        self.pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
        self.pololu_1.reset(self.pwm)

        self.pololu_2 = TB9051FTG(channel=CHANNEL5, freq=300, pin_in=MOTORS["pololu_2"]["enc_pins"], pin_out=MOTORS["pololu_2"]["driver_pins"])
        self.pololu_2.reset(self.pwm)

        self.pololu_3 = TB9051FTG(channel=CHANNEL6, freq=300, pin_in=MOTORS["pololu_3"]["enc_pins"], pin_out=MOTORS["pololu_3"]["driver_pins"])
        self.pololu_3.reset(self.pwm)

        self.pololu_4 = TB9051FTG(channel=CHANNEL7, freq=300, pin_in=MOTORS["pololu_4"]["enc_pins"], pin_out=MOTORS["pololu_4"]["driver_pins"])
        self.pololu_4.reset(self.pwm)

        ########################
        # INIT PID CONTROLLERS #
        ########################
        uaslog.debug("Init PID controllers...")
        self.pid_1 = PID(MOTORS["pololu_1"]["enc_pins"])
        self.pid_2 = PID(MOTORS["pololu_2"]["enc_pins"])
        self.pid_3 = PID(MOTORS["pololu_3"]["enc_pins"])
        self.pid_4 = PID(MOTORS["pololu_4"]["enc_pins"])

        uaslog.info("Motor Drive System init complete! Starting main routine...")
        
    def loop(self):
        try:
            while True:
                # READ JOYSTICK
                raw_ljs_x = wpi.analogRead(PIN_LJSX)
                raw_ljs_y = wpi.analogRead(PIN_LJSY)

                ljs_x, ljs_y = remap_range(raw_ljs_x, raw_ljs_y)
                

                uaslog.info("Starting Joystick Motor Control Test...")
                uaslog.info("Joystick will control wheels to move forward or backward.")

                

                
        except KeyboardInterrupt:
            uaslog.info("Motor Isolation Test Complete!")
            self.cleanup()
            sys.exit(0)

    def init_gpio(self):
            uaslog.info("Init GPIO...")
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
            uaslog.info("Init GPIO complete!")

    def cleanup(self):
        uaslog.info("Cleaning up driver system...")
        # reset motors
        self.pololu_1.reset(self.pwm)
        self.pololu_2.reset(self.pwm)
        self.pololu_3.reset(self.pwm)
        self.pololu_4.reset(self.pwm)

def main():
    test = JoystickControl()
    test.loop()
        
if __name__ == "__main__":
    main()