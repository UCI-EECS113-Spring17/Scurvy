import pytest
import logging
from pynq.iop.arduino_can_bus import Can,Message
import pynq.iop.arduino_can_bus as const

message = Message()
previous = Message()
c = Can()
c.reset(1)
logging.basicConfig(filename='get_message.log',level=logging.DEBUG)
logging.info("Starting logging")
while True:
    message = c.get_message()
    if message != previous:
        previous = message
        logging.info(message)