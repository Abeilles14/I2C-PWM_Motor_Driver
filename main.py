from pwm import PWM
from constants import *
from TB9051FTG import TB9051FTG

def main():
    FREQUENCY = 5 # Hz
    pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS,debug=True)
    pwm.setPWMFreq(FREQUENCY)

    # actuonixL16 = Motor(channel=CHANNEL0, freq=300)
    # actuonixL16.reset(pwm)
    # actuonixL16.setPWM(pwm, dutycycle=60)
    
    #### WINCH MOTOR ####
    # GOING FORWARD: PWM1 H PWM2 L EN H ENB L
    # setup up pwm1 and pwm2
    pololu1 = TB9051FTG(channel=CHANNEL2, freq=FREQUENCY, pin_in=POLOLU1_ENC, pin_out=TB9051FTG_PINS)
    pololu1.reset(pwm)
    # pololu1.forward(pwm, dutycycle=30)

    while True:
        direction = input("Enter f for fwd, b for bkwd, s for stop: ")
        if direction == "f":
            print("Going forward")
            pololu1.forward(pwm, dutycycle=30)
        elif direction == "b":
            print("Going Backward")
            pololu1.backward(pwm, dutycycle=30)
        elif direction == "s":
            print("Stopping")
            pololu1.stop(pwm)
    # pololu1.setPWM(pwm, dutycycle=30)


if __name__ == "__main__":
    main()
