# Register Addresses
MODE1           = 0x00
MODE2           = 0x01
SUBADR1         = 0x02
SUBADR2         = 0x03
SUBADR3         = 0x04
ALLCALLADR      = 0x05
LED0_ON_L       = 0x06
LED0_ON_H       = 0x07
LED0_OFF_L      = 0x08
LED0_OFF_H      = 0x09
ALLLED_ON_L     = 0xFA
ALLLED_ON_H     = 0xFB
ALLLED_OFF_L    = 0xFC
ALLLED_OFF_H    = 0xFD
PRESCALE        = 0xFE

# I2C parameter defaults
I2C_BUS = 0
I2C_DEV = "/dev/i2c-0"
I2C_CHIP = 0x40

# PCA9685
COUNTER_SIZE = 4096.0
CLK = 25000000.0
