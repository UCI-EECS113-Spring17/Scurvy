import constants
import OBD
import pytest

obd = OBD.OBD()
obd.ecu_req(constants.THROTTLE)