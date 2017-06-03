import constants
import OBD
import pytest
import time
import logging

from pynq.board import Switch

CANSPEED_125 = 7
CANSPEED_250 = 3
CANSPEED_500 = 1

obd = OBD.OBD(CANSPEED_500, logger=False)
time.sleep(2)
switch_1 = Switch(0)
switch_2 = Switch(1)
logging.basicConfig(level=logging.DEBUG)

while True:
    inp = (switch_1.read() << 1) | switch_2.read()
    if inp == 3:
        obd.ecu_req(constants.VEHICLE_SPEED)
    elif inp == 2:
        obd.ecu_req(constants.THROTTLE)
    elif inp == 1:
        obd.ecu_req(constants.ENGINE_RPM)
    else:
        obd.ecu_req(constants.O2_VOLTAGE)
    time.sleep(1)