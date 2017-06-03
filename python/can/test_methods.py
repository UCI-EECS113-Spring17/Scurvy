import pytest
from pynq.iop.arduino_can_bus import Can,Message
import pynq.iop.arduino_can_bus as const

message = Message()
message.id = 500
message.rtr = 17
message.length = 23
message.data = [[1,2,3,4],[5,6,7,8]]
c = Can()


def test_mailbox_rw():
    c._write_command(0)
    c._write_message(message)
    data = c._read_message()
    assert str(data) == str(message), \
        "data and message string mismatched"

def test_commands_reset_to_0x00():
    c._write_command(int('0x03',16))
    assert c._read_command() == 0, \
        "Microblaze should have written back 0x00"


def test_read_write_message():
    c._write_message(message)
    c._write_command(const.CMD_TEST_MESSAGE_WRITE)
    c._wait_for_command()
    c._write_command(const.CMD_TEST_MESSAGE_READ)
    c._wait_for_command()
    data = c._read_message()
    assert str(data) == str(message), \
        "data and message string mismatched"