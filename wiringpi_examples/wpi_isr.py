import odroid_wiringpi as wiringpi
PIN_TO_SENSE = 23

def gpio_callback():
    print("GPIO_CALLBACK!")

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN_TO_SENSE, 0)
wiringpi.pullUpDnControl(PIN_TO_SENSE, wiringpi.GPIO.PUD_UP)

wiringpi.wiringPiISR(PIN_TO_SENSE, wiringpi.GPIO.INT_EDGE_BOTH, gpio_callback)

while True:
    print(wiringpi.digitalRead(PIN_TO_SENSE))
    # wiringpi.delay(2000)