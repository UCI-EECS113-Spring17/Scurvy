import pytest
import time
from pynq.iop.arduino_can_bus import Can,Message


message = Message()
message.id = 500
message.rtr = 17
message.length = 23
message.data = [[1,2,3,4],[5,6,7,8]]
can = Can()

can.send_message(message)