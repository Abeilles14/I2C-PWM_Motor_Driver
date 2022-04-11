from pwm import PWM
from constants import *
from TB9051FTG import SingleTB9051FTG
from PCA9685 import PCA9685

def main():
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS,debug=True)

    actuonixL16_1 = PCA9685(channel=CHANNEL0, freq=300)
    actuonixL16_1.reset(pwm)
    
    hext900_1 = PCA9685(channel=CHANNEL1, freq=50)
    hext900_1.reset(pwm)
    
    #### WINCH MOTOR ####
    pololu_1 = TB9051FTG(channel=CHANNEL2, freq=5, pin_in=POLOLU1_ENC, pin_out=TB9051FTG_PINS)
    pololu_1.reset(pwm)

    while True:
        motor = input("Enter p for pololu, a for actuator, h for hextronik: ")
        if motor == "p":
            FREQUENCY=5
            pwm.setPWMFreq(FREQUENCY)
            hext900_1.reset(pwm)
            actuonixL16_1.reset(pwm)

            direction = input("Enter f for fwd, b for bkwd, s for stop: ")

            if direction == "f":
                print("Going forward")
                pololu_1.forward(pwm, dutycycle=30)
            elif direction == "b":
                print("Going Backward")
                pololu_1.backward(pwm, dutycycle=30)
            elif direction == "s":
                print("Stopping")
                pololu_1.stop(pwm)
        elif motor == "a":
            FREQUENCY=300
            pwm.setPWMFreq(FREQUENCY)
            hext900_1.reset(pwm)
            pololu_1.reset(pwm)

            direction = input("Enter o for out, i for in: ")

            if direction == "i":
                print("Going in")
                actuonixL16_1.setPWM(pwm, dutycycle=30)
            elif direction == "o":
                print("Going out")
                actuonixL16_1.setPWM(pwm, dutycycle=60)
        elif motor == "h":
            FREQUENCY=50
            pwm.setPWMFreq(FREQUENCY)
            pololu_1.reset(pwm)
            actuonixL16_1.reset(pwm)

            direction = input("Enter f for fwd, b for bkwd: ")

            if direction == "f":
                print("Going forward")
                hext900_1.setPWM(pwm, dutycycle=3)
            elif direction == "b":
                print("Going Backward")
                hext900_1.setPWM(pwm, dutycycle=11)

if __name__ == "__main__":
    main()
