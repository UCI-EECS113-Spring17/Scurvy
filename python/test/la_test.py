import pytest
import time
from pynq.iop.arduino_can_bus import Can,Message


@pytest.fixture
def message():
    message = Message()
    message.id = int('0x7DF', 16)
    message.rtr = 0
    message.length = 8
    message.data = [[1,2,3,4],[5,6,7,8]]
    return message


def test_mailbox_rw(message):
    can = Can()
    can._write_message(message)
    message_2 = can._read_message()
    print("M1: ", message)
    print("M2: ", message_2)
    assert message == message_2


if __name__ == "__main__":
    msg = message()
    can = Can()
    can.send_message(msg)
