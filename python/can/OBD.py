import time
import logging
from pynq.iop.arduino_can_bus import Can,Message
import constants

class OBD:

    def __init__(self, speed: int, logger = None):
        self.can = Can()
        self.can.reset(speed)
        if logger:
            self.logger = logger
        else:
            logger = logging.basicConfig(filename='obd.log',level=logging.INFO)

    def ecu_req(self, pid) -> bool:
        '''Queries the CAN bus using the OBD protocol for ecu data
        
        Parameters
            pid: the pid to request from the ecu
        
        Returns
            Returns True if a message was received from the ecu
        '''
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
        self.logger.debug("Sending message: %s", message)
        self.can.send_message(message)

        # We only want to try and get a message if the interrupt signals one is waiting
        if self.can.check_message():
            message = self.can.get_message()
            if message.data[0][2] == constants.ENGINE_RPM:
                engine_data = ((message.data[0][3]*256) + message.data[1][0])/4
                self.logger.info("RPM: %s", engine_data)

            elif message.data[0][2] == constants.ENGINE_COOLANT_TEMP:
                engine_data = message.data[0][3] - 40
                self.logger.info("COOLANT: %s", engine_data)

            elif message.data[0][2] == constants.VEHICLE_SPEED:
                engine_data = message.data[0][3]
                self.logger.info("SPEED: %s", engine_data)

            elif message.data[0][2] == constants.MAF_SENSOR:
                engine_data = ((message.data[0][3]*256) + message.data[1][0])/100
                self.logger.info("MAF: %s", engine_data)

            elif message.data[0][2] == constants.THROTTLE:
                engine_data = (message.data[0][3]*100)/255;
                self.logger.info("THROTTLE: %s", engine_data)
            self.logger.debug("Received message: %s", message)
            return True
        return False
