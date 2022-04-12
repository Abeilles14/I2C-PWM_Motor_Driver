# motor specs as a dict
MOTORS = {
    "pololu1": {
        "position": "front left",
        "frequency": 5, # 300 rpm
        "enc_pins": [15, 16], # encA, encB
        "driver_pins": [2, 0, 7], # dir, en, enb
    },
    "actuonixL16R": {
        "frequency": 300,   # hz
        "dc range": 30,     # %
        "stroke": 140,   # mm
    },
}