import struct
import logging
import binascii
import json

from pynq import MMIO
from pynq.iop import request_iop
from pynq.iop import iop_const
from pynq.iop import Arduino_IO


MESSAGE_PACK = (">HBB", ">BBBB", ">BBBB")
CAN_BUS_BIN = "arduino_can_bus.bin"
ARDUINO_IF_ID = 3

CMD_CLEARED = int('0x0', 16)
CMD_RESET = int('0x01', 16)
CMD_READ = int('0x02', 16)
CMD_WRITE = int('0x03', 16)
CMD_BIT_MODIFY = int('0x04', 16)
CMD_READ_STATUS = int('0x05', 16)
CMD_GET_MESSAGE = int('0x06', 16)
CMD_SEND_MESSAGE = int('0x07', 16)
CMD_CHECK_MESSAGE = int('0x08', 16)

CMD_TEST_MESSAGE_WRITE = int('0xFF', 16)
CMD_TEST_MESSAGE_READ = int('0xFE', 16)

def binary(val: int):
    print('{0:032b}'.format(val))


class Message:
    def __init__(self):
        self.id = 0
        self.rtr = 0
        self.length = 0
        self.data = [[0,0,0,0],[0,0,0,0]]

    def __str__(self):
        return json.dumps({'id':self.id, 'rtr':self.rtr, 'length':self.length, 'data':self.data})

    def __eq__(self, value):
        return str(self) == str(value) 

    def __ne__(self, value):
        return not self.__eq__(value)


class Can:
    '''Object representing pure IOP communication.'''

    def __init__(self):
        self.iop = request_iop(ARDUINO_IF_ID, CAN_BUS_BIN)
        self.mmio = self.iop.mmio
        self.mmio.debug=False
        self.iop.start()

    def _mailbox_write(self, offset, word):
        self.mmio.write(iop_const.MAILBOX_OFFSET+(offset*4), word)

    def _mailbox_read(self, offset):
        return self.mmio.read(iop_const.MAILBOX_OFFSET+offset*4)

    def _write_message(self, message: Message):
        logging.debug("Writing Message: ")
        word = struct.pack(MESSAGE_PACK[0], message.id, message.rtr, message.length)
        logging.debug(binascii.hexlify(word))
        word = struct.unpack('>L',word)[0]
        self._mailbox_write(0, word)
        for i in range(2):
            word = struct.pack(MESSAGE_PACK[i+1],
                            message.data[i][0],
                            message.data[i][1],
                            message.data[i][2],
                            message.data[i][3])
            logging.debug(binascii.hexlify(word))
            word = struct.unpack('>L',word)[0]
            self._mailbox_write(i+1, word)

    def _read_message(self):
        logging.debug("Reading Message: ")
        message = Message()
        word = self._mailbox_read(0)
        word = struct.pack('>L',word)
        logging.debug(binascii.hexlify(word))
        message.id, message.rtr, message.length = struct.unpack(MESSAGE_PACK[0], word)
        for i in range(2):
            word = self._mailbox_read(i+1)
            word = struct.pack('>L',word)
            logging.debug(binascii.hexlify(word))
            message.data[i][0], message.data[i][1], message.data[i][2], message.data[i][3] = struct.unpack(MESSAGE_PACK[i+1],word)
        return message

    def _write_command(self, cmd: int):
        self.mmio.write(iop_const.MAILBOX_OFFSET +
            iop_const.MAILBOX_PY2IOP_CMD_OFFSET, cmd)

    def _read_command(self):
        return self.mmio.read(iop_const.MAILBOX_OFFSET+iop_const.MAILBOX_PY2IOP_CMD_OFFSET)

    def _wait_for_command(self):
        while(self._read_command() != 0):
            pass

    def send_message(self, message: Message):
        self._write_message(message)
        self._write_command(CMD_SEND_MESSAGE)
        self._wait_for_command()

    def get_message(self):
        self._write_command(CMD_GET_MESSAGE)
        self._wait_for_command()
        return self._read_message()
    
    def bit_modify(self, address, mask, data):
        self._mailbox_write(0, address)
        self._mailbox_write(1, mask)
        self._mailbox_write(2, data)
        self._write_command(CMD_BIT_MODIFY)
        self._wait_for_command()

    def reset(self, speed: int):
        self._mailbox_write(0, speed)
        self._write_command(CMD_RESET)
        self._wait_for_command()
    
    def read_status(self, data_type: int):
        self._mailbox_write(0, data_type)
        self._write_command(CMD_READ_STATUS)
        self._wait_for_command()
        return self._mailbox_read(0)

    def read(self, speed: int):
        self._mailbox_write(0, speed)
        self._write_command(CMD_READ)
        self._wait_for_command()
    
    def write(self, data: int):
        self._mailbox_write(0, data)
        self._write_command(CMD_WRITE)
        self._wait_for_command()
        return self._mailbox_read(0)

    def check_message(self):
        self._mailbox_write(0, 2)
        self._write_command(CMD_CHECK_MESSAGE)
        self._wait_for_command()
        return False if self._mailbox_read(0) else True
