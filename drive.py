# mecanum wheel control interface

from constants import *

def setMotorTargets(left_vrx, left_vry, right_vrx, target_pololu, debug=False):

    # controls FWD/BCK directions
    target_pololu[1] += left_vry
    target_pololu[2] += left_vry
    target_pololu[3] += left_vry
    target_pololu[4] += left_vry

    # target_pololu[1] += left_vry * ACCEL_MULTIPLIER
    # target_pololu[2] += left_vry * ACCEL_MULTIPLIER
    # target_pololu[3] += left_vry * ACCEL_MULTIPLIER
    # target_pololu[4] += left_vry * ACCEL_MULTIPLIER

    # controls L/R side of rover
    if left_vry > 0:
        # forward
        if left_vrx > 0:
            if debug:
                print("forward right")
            # right
            # slow down the right wheels only
            # target_pololu[1] += left_vrx
            target_pololu[2] += left_vrx * 3
            # target_pololu[3] += left_vrx
            target_pololu[4] += left_vrx * 3
        elif left_vrx < 0:
            if debug:
                print("forward left")
            # left
            # slow down the left wheels only
            target_pololu[1] += left_vrx * 3
            # target_pololu[2] += left_vrx
            target_pololu[3] += left_vrx * 3
            # target_pololu[4] += left_vrx
    elif left_vry < 0:
        # backward
        if left_vrx > 0:
            if debug:
                print("back right")
            # right
            # slow down the right wheels only
            # target_pololu[1] += left_vrx
            target_pololu[2] += left_vrx * 3
            # target_pololu[3] += left_vrx
            target_pololu[4] += left_vrx * 3
        elif left_vrx < 0:
            if debug:
                print("back left")
            # left
            # slow down the left wheels only
            target_pololu[1] -= left_vrx * 3
            # target_pololu[2] += left_vrx
            target_pololu[3] -= left_vrx * 3
            # target_pololu[4] += left_vrx
    
    return target_pololu

# def setSpinMotorTargets(trigger_l, trigger_r, target_pololu):
#     if trigger_l > 0.2:
#         print("spin left")
#         # spin left (-+-+)
#         target_pololu[1] -= trigger_l
#         target_pololu[2] += trigger_l
#         target_pololu[3] -= trigger_l
#         target_pololu[4] += trigger_l
#     elif trigger_r > 0.2:
#         print("spin right")
#         # spin left (+-+-)
#         target_pololu[1] += trigger_r
#         target_pololu[2] -= trigger_r
#         target_pololu[3] += trigger_r
#         target_pololu[4] -= trigger_r

#     return target_pololu