import pytest
import time
from pynq.iop.arduino_can_bus import Can,Message
import pynq.iop.arduino_can_bus as const

message = Message()
previous = Message()
c = Can()
c.reset(1)
while True:
    message = c.get_message()
    if message != previous:
        previous = message
        print(message)