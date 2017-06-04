import pytest
import logging
import time
from pynq.iop.arduino_can_bus import Can,Message
import constants

message = Message()
message.id = int('0x631', 16)
message.rtr = 0
message.length = 8
message.data[0][0] = int('0x40', 16)
message.data[0][1] = int('0x05', 16)
message.data[0][2] = int('0x30', 16)
message.data[0][3] = int('0xFF', 16)
message.data[1][0] = int('0x00', 16)
message.data[1][1] = int('0x40', 16)
message.data[1][2] = int('0x00', 16)
message.data[1][3] = int('0x00', 16)

c = Can()
c.reset(1)
logging.basicConfig(level=logging.DEBUG)
logging.info("Starting logging")
while True:
    c.bit_modify(constants.CANCTRL, int('11100000', 2), 0)
    logging.info(message)
    c.send_message(message)
    time.sleep(1)