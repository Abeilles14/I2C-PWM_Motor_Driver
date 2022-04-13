# motor specs as a dict
MOTORS = {
    "pololu_0": {
        "position": "winch",
        "frequency": 300, # 300 rpm
        "enc_pins": [],
        "driver_pins": [27, 26, 31], # pwm1, pwm2, enb
    },
    "pololu_1": {
        "position": "front left",
        "frequency": 300, # 300 rpm
        "enc_pins": [4,5], # encA, encB (15,16)
        "driver_pins": [2, 0, 7], # dir, en, enb
    },
    "actuonix_1": {
        "position": "idk",
        "frequency": 300,   # hz
        "dc low": 30,     # 30-60%
        "dc high": 60,
        "stroke": 140,   # mm
    },
    "turnigy_1": {
        "position": "idk",
        "frequency": 300,   # hz
        "dc low": 28,     # 28-64%
        "dc high": 64,
    }
}