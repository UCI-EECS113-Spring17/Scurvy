import time
import logging
from pynq.iop.arduino_can_bus import Can,Message
import constants

class OBD:

    def __init__(self, speed: int, logger = True):
        self.can = Can()
        self.can.reset(speed)
        if logger:
            logging.basicConfig(filename='obd.log',level=logging.INFO)

    def ecu_req(self, pid):
        message = Message()
        engine_data = None

        message.id = constants.PID_REQUEST
        message.rtr = 0
        message.length = 8
        message.data = [
            [2, 1, pid, 0],
            [0, 0, 0, 0]
        ]

        self.can.bit_modify(constants.CANCTRL, int('0b11100000', 2), 0)
        logging.debug("Sending message: %s", message)
        self.can.send_message(message)
        if self.can.check_message():
            message = self.can.get_message()
            if message.data[0][2] == constants.ENGINE_RPM:
                engine_data = ((message.data[0][3]*256) + message.data[1][0])/4
                logging.info("Engine RPM: %s", engine_data)
            elif message.data[0][2] == constants.ENGINE_COOLANT_TEMP:
                engine_data = message.data[0][3] - 40
                logging.info("Engine Coolant Temp (C): %s", engine_data)
            elif message.data[0][2] == constants.VEHICLE_SPEED:
                engine_data = message.data[0][3]
                logging.info("Vehicle Speed: %s", engine_data)
            elif message.data[0][2] == constants.MAF_SENSOR:
                engine_data = ((message.data[0][3]*256) + message.data[1][0])/100
                logging.info("MAF Status: %s", engine_data)
            elif message.data[0][2] == constants.THROTTLE:
                engine_data = (message.data[0][3]*100)/255;
                logging.info("Throttle: %s", engine_data)
            logging.debug("Received message: %s", message)
