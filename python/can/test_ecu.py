import constants
import OBD
import time
import shutil
import sys
import logging

import requests

from pynq.board import Button
from pynq.board import LED

LED_POSTING = LED(3)
LED_RUNNING = LED(0)
LED_2 = LED(2)
LED_1 = LED(1)

CANSPEED_125 = 7
CANSPEED_250 = 3
CANSPEED_500 = 1

SERVER_URL = 'https://scurvy-can-bus.herokuapp.com/logs'
# SERVER_URL = 'http://192.168.1.82:8080/logs'

STOP_COUNT = 20
LOG_FILE = "ecu.log"
logger = logging.getLogger(__name__)

# File logging
fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setLevel(logging.INFO)
formatter = logging.Formatter('')
fileHandler.setFormatter(formatter)

# Console logging
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG)

logger.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)
# logger.addHandler(consoleHandler)
obd = None

def reset():
    global obd
    global logger
    obd = OBD.OBD(CANSPEED_500, logger=logger)
    time.sleep(2)


def worker(counter: int):
    global obd
    result = False
    if counter % 10 == 0:
        result = obd.ecu_req(constants.MAF_SENSOR)
    elif counter % 10 == 1:
        result = obd.ecu_req(constants.ENGINE_COOLANT_TEMP)
    elif counter % 10 == 2:
        result = obd.ecu_req(constants.O2_VOLTAGE)
    elif counter % 10 == 3:
        result = obd.ecu_req(constants.THROTTLE)
    elif counter % 10 == 4:
        result = obd.ecu_req(constants.VEHICLE_SPEED)
    elif counter % 10 == 5:
        result = obd.ecu_req(constants.ENGINE_RPM)

    return result

def serve_logs():
    '''Attempts to post logs to the server for use
    
    Note
        Waits for a successful connection to the internet first

    Returns
        Return True if post was successful
    '''
    global logger
    global LOG_FILE
    try:
        requests.get("http://google.com", timeout=4)
    except requests.exceptions.RequestException:
        return False

    with open(LOG_FILE, 'rb') as f:
        try:
            res = requests.post(SERVER_URL,f.read(), timeout=10)
            if res:
                logger.debug("Log: {} posted successfully, moving".format(LOG_FILE))
                # Copy the log file for safe keeping
                shutil.copy(LOG_FILE, "done/"+str(time.time())+".log")
        except:
            logger.debug("Timed Out Posting Log")
            return False

    # Truncate the log file
    with open(LOG_FILE, 'w') as file:
        pass
    return True

if __name__ == "__main__":
    rst = Button(0)
    counter = 0
    timer = 0 # Keep track of how long it's been since we've gotten a log
    run = False # Loop flag
    posted = False

    LED_1.off()
    LED_2.off()
    LED_POSTING.off()
    LED_RUNNING.off()

    logger.debug("Starting now")
    while True:
        time.sleep(1)
        if run:
            LED_1.on()
            posted = False
            counter += 1
            if worker(counter): # If we get a message successfully, reset timer
                timer = 0
            else: # otherwise, keep track of failed messages (eg when car is off)
                timer += 1
            LED_1.off()
        elif not posted:
            LED_POSTING.on()
            posted = serve_logs()

        # Stop running when we encounter too many failed messages
        if timer >= STOP_COUNT:
            LED_RUNNING.off()
            logger.debug("Stopped running, serving now")
            run = False
            timer = 0
        elif rst.read() == 1: # on Button press start running
            LED_RUNNING.on()
            LED_POSTING.off()
            logger.debug("Started running")
            reset()
            run = True
            counter = 0