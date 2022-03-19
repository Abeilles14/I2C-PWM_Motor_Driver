from constants import *

# calculate OFF count from duty cycle and delay %
def getCounterValues(delay, dc):
    on_count = round(delay*COUNTER_SIZE/100)
    off_count = on_count + round(dc*COUNTER_SIZE/100)

    return on_count, off_count
