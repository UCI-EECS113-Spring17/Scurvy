import constants
import OBD
import pytest

CANSPEED_125 = 7
CANSPEED_250 = 3
CANSPEED_500 = 1

obd = OBD.OBD(CANSPEED_500)
obd.ecu_req(constants.THROTTLE)