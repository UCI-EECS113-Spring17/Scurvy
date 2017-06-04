import logging
import time
from pynq.iop.arduino_can_bus import Can,Message
import pynq.iop.arduino_can_bus as const

message = Message()
c = Can()
c.reset(1)
while True:
    print(c.check_message())
    time.sleep(0.5)