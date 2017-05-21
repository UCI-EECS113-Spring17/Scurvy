import pytest
from pynq.iop.arduino_can_bus import Can,Message

message = Message()
message.id = 500
message.rtr = 17
message.length = 23
message.data = [[1,2,3,4],[5,6,7,8]]


def test_mailbox_rw():
    c = Can()
    c._write_command(0)
    c._write_message(message)
    data = c._read_message()
    assert str(data) == str(message), \
        "data and message string mismatched"