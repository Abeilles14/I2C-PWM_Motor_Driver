from constants import *

# calculate OFF count from duty cycle and delay %
def getCounterValues(delay, dc):
    on_count = round(delay*COUNTER_SIZE/100)
    off_count = on_count + round(dc*COUNTER_SIZE/100)

    return on_count, off_count

# calculate duty cycle from angle
def getActuatorDCfromLength(len):
    dc = 30 + round(len*DC_RANGE/STROKE)
    return dc

# TODO
def getMotorDCfromAngle(angle):
    return

def pwmToDc(range):
    return (100*(range + 1)/256)
