import constants
import OBD
import pytest
import time
import logging


CANSPEED_125 = 7
CANSPEED_250 = 3
CANSPEED_500 = 1

logging.basicConfig(filename="ecu_quick.log", level=logging.INFO)
obd = OBD.OBD(CANSPEED_500, logger=False)
counter = 0
time.sleep(2)

while True:
    if counter % 10 == 0:
        obd.ecu_req(constants.VEHICLE_SPEED)
    elif counter % 10 == 1:
        obd.ecu_req(constants.THROTTLE)
    elif counter % 10 == 2:
        obd.ecu_req(constants.ENGINE_RPM)
    elif counter % 10 == 3:
        obd.ecu_req(constants.ENGINE_COOLANT_TEMP)
    elif counter % 10 == 4:
        obd.ecu_req(constants.O2_VOLTAGE)
    elif counter % 10 == 5:
        obd.ecu_req(constants.MAF_SENSOR)

    counter += 1
