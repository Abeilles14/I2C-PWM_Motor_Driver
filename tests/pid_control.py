import time
import sys
import math
import logging
import odroid_wiringpi as wpi
from pwm import PWM
from uas_control_system.constants import *
from uas_control_system.motor_specs import MOTORS
from uas_control_system.TB9051FTG import TB9051FTG
from uas_control_system.PCA9685 import PCA9685
from uas_control_system.utils import remap_range
from uas_control_system.PID_controller import PID
from uas_control_system.encoder import Encoder

logging.getLogger("Adafruit_I2C.Device.Bus.{0}.Address.{1:#0X}".format(0, 0X40)).setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
uaslog = logging.getLogger("UASlogger")
        
class PIDControl:
    def __init__(self):
        ############################
        # INIT MOTOR TARGET VALUES #
        ############################
        self.target_pololu = [0, 0, 0, 0, 0] # p0, p1, p2, p3, p4 = [w, fl, fr, rl, rr]

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
        # self.pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
        # self.pololu_1.reset(self.pwm)

        # self.pololu_2 = TB9051FTG(channel=CHANNEL5, freq=300, pin_in=MOTORS["pololu_2"]["enc_pins"], pin_out=MOTORS["pololu_2"]["driver_pins"])
        # self.pololu_2.reset(self.pwm)

        self.pololu_3 = TB9051FTG(channel=CHANNEL6, freq=300, pin_in=MOTORS["pololu_3"]["enc_pins"], pin_out=MOTORS["pololu_3"]["driver_pins"])
        self.pololu_3.reset(self.pwm)

        # self.pololu_4 = TB9051FTG(channel=CHANNEL7, freq=300, pin_in=MOTORS["pololu_4"]["enc_pins"], pin_out=MOTORS["pololu_4"]["driver_pins"])
        # self.pololu_4.reset(self.pwm)

        ########################
        # INIT PID CONTROLLERS #
        ########################
        uaslog.debug("Init PID controllers...")
        # self.pid_1 = PID(MOTORS["pololu_1"]["enc_pins"], debug=True)
        # self.pid_2 = PID(MOTORS["pololu_2"]["enc_pins"])
        self.pid_3 = PID(MOTORS["pololu_3"]["enc_pins"])
        # self.pid_4 = PID(MOTORS["pololu_4"]["enc_pins"])

        uaslog.info("Motor Drive System init complete! Starting main routine...")
        
    def loop(self):
        uaslog.info("Starting PID Control Test...")
        uaslog.info("Each Motor Will Move to Target 1500.")

        # self.target_pololu[1] = 1500
        # self.target_pololu[2] = 1500
        self.target_pololu[3] = 1500
        # self.target_pololu[4] = 1500

        try:
            while True:
                
                # self.pid_1.loop(round(self.target_pololu[1]))
                # self.pid_2.loop(round(self.target_pololu[2]))
                self.pid_3.loop(round(self.target_pololu[3]))
                # self.pid_4.loop(round(self.target_pololu[4]))

                # signal the motors
                # if self.pid_1.getDir() == -1:
                #     self.pololu_1.forward(self.pwm, dutycycle=self.pid_1.getDc())
                # elif self.pid_1.getDir() == 1:
                #     self.pololu_1.backward(self.pwm, dutycycle=self.pid_1.getDc())
                
                # if self.pid_2.getDir() == -1:
                #     self.pololu_2.forward(self.pwm, dutycycle=self.pid_2.getDc())
                # elif self.pid_2.getDir() == 1:
                #     self.pololu_2.backward(self.pwm, dutycycle=self.pid_2.getDc())

                if self.pid_3.getDir() == -1:
                    self.pololu_3.forward(self.pwm, dutycycle=self.pid_3.getDc())
                elif self.pid_3.getDir() == 1:
                    self.pololu_3.backward(self.pwm, dutycycle=self.pid_3.getDc())

                # if self.pid_4.getDir() == -1:
                #     self.pololu_4.forward(self.pwm, dutycycle=self.pid_4.getDc())
                # elif self.pid_4.getDir() == 1:
                #     self.pololu_4.backward(self.pwm, dutycycle=self.pid_4.getDc())
                
                print(f"curr pos: [{self.pid_3.getPos()}, ]")
                # print(f"curr pos: [{self.pid_1.getPos()}, {self.pid_2.getPos()}, {self.pid_3.getPos()}, {self.pid_4.getPos()}, ]")
                
        except KeyboardInterrupt:
            uaslog.info("PID Control Test Complete!")
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
        # self.pololu_1.reset(self.pwm)
        # self.pololu_2.reset(self.pwm)
        self.pololu_3.reset(self.pwm)
        # self.pololu_4.reset(self.pwm)

def main():
    test = PIDControl()
    test.loop()
        
if __name__ == "__main__":
    main()