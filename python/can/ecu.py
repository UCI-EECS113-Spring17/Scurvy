#!python3.6
import constants
import OBD
import pytest
import time
import logging


CANSPEED_125 = 7
CANSPEED_250 = 3
CANSPEED_500 = 1


obd = OBD.OBD(CANSPEED_500, logger=False)
counter = 0
time.sleep(2)

# Get all available pids from constants
pids = list(constants.Sensor.keys())
num_pids = len(pids)

while True:
    logging.basicConfig(filename="ecu_2.log", level=logging.INFO)
    obd.ecu_req(pids[counter % num_pids])
    counter += 1

# def configure_logger(logger_name: str, level: int):
#     logger = logging.getLogger(logger_name)
#     logger.addHandler(logging.FileHandler(filename="ecu.log",mode='w',encoding='utf8',delay=True))
#     logger.addHandler(logging.Soc)