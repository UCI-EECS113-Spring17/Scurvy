import constants
import OBD
import pytest
import time
import logging
from pynq.board import Switch
from pynq.board import Button


CANSPEED_125 = 7
CANSPEED_250 = 3
CANSPEED_500 = 1
logging.basicConfig(filename="ecu_log.log", level=logging.INFO)
obd = None
en = True


def reset():
    global obd
    global en
    canspeed = 0
    speed_select0 = Switch(0)
    speed_select1 = Switch(1)
    val = speed_select1.read() << 1 | speed_select0.read()

    en = True
    if val == 0:
        canspeed = CANSPEED_500
    elif val == 1:
        canspeed = CANSPEED_250
    elif val == 2:
        canspeed = CANSPEED_125
    else:
        en = False

    logging.debug(canspeed)
    obd = OBD.OBD(canspeed, logger=False)
    time.sleep(2)


def run(counter: int):
    global obd
    if counter % 10 == 0:
        obd.ecu_req(constants.VEHICLE_SPEED)
    if counter % 10 == 1:
        obd.ecu_req(constants.THROTTLE)
    if counter % 10 == 2:
        obd.ecu_req(constants.ENGINE_RPM)
    if counter % 10 == 3:
        obd.ecu_req(constants.ENGINE_COOLANT_TEMP)
    if counter % 10 == 4:
        obd.ecu_req(constants.O2_VOLTAGE)
    if counter % 10 == 5:
        obd.ecu_req(constants.MAF_SENSOR)

    time.sleep(0.5)

if __name__ == "__main__":
    rst = Button(0)
    counter = 0
    reset()

    while True:
        if rst.read():
            logging.debug("Resetting")
            reset()
            counter = 0
        elif en:
            run(counter)
            counter += 1