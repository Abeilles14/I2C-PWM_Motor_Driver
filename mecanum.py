# mecanum wheel control interface

def setMotorTargets(sc_vrx, sc_vry, target_pololu):
    if (sc_vrx < 0.2 and sc_vrx > -0.2) and (sc_vry < 0.2 and sc_vry > -0.2):
        print("idle")
    elif (sc_vrx < 0.2 and sc_vrx > -0.2) and sc_vry >= 0.0:
        print("forward")
        # forward (++++)
        target_pololu[1] += sc_vry
        target_pololu[2] += sc_vry
        target_pololu[3] += sc_vry
        target_pololu[4] += sc_vry
    elif (sc_vrx < 0.2 and sc_vrx > -0.2) and sc_vry <= 0.0:
        print("backward")
        # backward (----)
        target_pololu[1] -= sc_vry
        target_pololu[2] -= sc_vry
        target_pololu[3] -= sc_vry
        target_pololu[4] -= sc_vry
    elif sc_vrx <= 0.0 and (sc_vry < 0.2 and sc_vry > -0.2):
        print("left")
        # left (-++-)
        target_pololu[1] -= sc_vrx
        target_pololu[2] += sc_vrx
        target_pololu[3] += sc_vrx
        target_pololu[4] -= sc_vrx
    elif sc_vrx >= 0.0 and (sc_vry < 0.2 and sc_vry > -0.2):
        print("right")
        # right (+--+)
        target_pololu[1] += sc_vrx
        target_pololu[2] -= sc_vrx
        target_pololu[3] -= sc_vrx
        target_pololu[4] += sc_vrx
    elif sc_vrx <= -0.2 and sc_vry >= 0.0:
        print("forward left")
        # forward left (0++0)
        target_pololu[1] -= sc_vrx
        target_pololu[2] += sc_vry
        target_pololu[3] += sc_vry
        target_pololu[4] -= sc_vrx
    elif sc_vrx >= 0.2 and sc_vry >= 0.0:
        print("forward right")
        # forward right (+00+)
        target_pololu[1] += sc_vry
        target_pololu[2] -= sc_vrx
        target_pololu[3] -= sc_vrx
        target_pololu[4] += sc_vry
    elif sc_vrx <= -0.2 and sc_vry <= 0.0:
        print("backward left")
        # backward left (-00-)
        target_pololu[1] -= sc_vry
        target_pololu[2] += sc_vrx
        target_pololu[3] += sc_vrx
        target_pololu[4] -= sc_vry
    elif sc_vrx >= 0.2 and sc_vry <= 0.0:
        print("backward right")
        # backward right (0--0)
        target_pololu[1] += sc_vry
        target_pololu[2] -= sc_vrx
        target_pololu[3] -= sc_vrx
        target_pololu[4] += sc_vry
    else:
        print("ERROR: Direction not supported, sorry my code kinda sucks")
        
    return target_pololu