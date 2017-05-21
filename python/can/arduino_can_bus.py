import struct
from pynq import MMIO
from pynq.iop import request_iop
from pynq.iop import iop_const
from pynq.iop import Arduino_IO


MESSAGE_PACK = (">HBB", ">BBBB", ">BBBB")
CAN_BUS_BIN = "arduino_can_bus.bin"
ARDUINO_IF_ID = 3

CMD_RESET = int('0xFF', 16)
CMD_READ = int('0xFE', 16)
CMD_WRITE = int('0xFD', 16)
CMD_BIT_MODIFY = int('0xFC', 16)
CMD_READ_STATUS = int('0xFB', 16)
CMD_GET_MESSAGE = int('0xEF', 16)
CMD_SEND_MESSAGE = int('0xEE', 16)
CMD_CHECK_MESSAGE = int('0xED', 16)

class Message:
    def __init__(self):
        self.id = 0
        self.rtr = 0
        self.length = 0
        self.data = [[0,0,0,0],[0,0,0,0]]

    def __str__(self):
        return "Message< id: {}, rtr: {}, length: {}, data: {}".format(self.id,self.rtr,self.length,self.data)


class Can:
    '''Object representing pure IOP communication.'''

    def __init__(self):
        self.iop = request_iop(ARDUINO_IF_ID, CAN_BUS_BIN)
        self.mmio = self.iop.mmio
        self.mmio.debug=True
        self.iop.start()

    def _write_message(self, message: Message):
        word = struct.pack(MESSAGE_PACK[0], message.id, message.rtr, message.length)
        word = struct.unpack('>l',word)[0]
        self.mmio.write(iop_const.MAILBOX_OFFSET, word)
        for i in range(2):
            word = struct.pack(MESSAGE_PACK[i+1],
                            message.data[i][0],
                            message.data[i][1],
                            message.data[i][2],
                            message.data[i][3])
            word = struct.unpack('>l',word)[0]
            self.mmio.write(iop_const.MAILBOX_OFFSET+(i+1)*4, word)

    def _read_message(self):
        message = Message()
        word = self.mmio.read(iop_const.MAILBOX_OFFSET)
        word = struct.pack('>l',word)
        message.id, message.rtr, message.length = struct.unpack(MESSAGE_PACK[0], word)
        for i in range(2):
            word = self.mmio.read(iop_const.MAILBOX_OFFSET+(i+1)*4)
            word = struct.pack('>l',word)
            message.data[i][0], message.data[i][1], message.data[i][2], message.data[i][3] = struct.unpack(MESSAGE_PACK[i+1],word)
        return message

    def _write_command(self, cmd: int):
        self.mmio.write(iop_const.MAILBOX_OFFSET +
            iop_const.MAILBOX_PY2IOP_CMD_OFFSET, cmd)

    def _wait_for_command(self, cmd: int):
        while(self.mmio.read(
                iop_const.MAILBOX_OFFSET+
                iop_const.MAILBOX_PY2IOP_CMD_OFFSET) != cmd):
            pass

    def send_message(self):
        self._write_command(CMD_SEND_MESSAGE)


    def get_message(self):
        self._write_command(CMD_GET_MESSAGE)
        self._wait_for_command(CMD_GET_MESSAGE)
        self._read_message()
    
    def bit_modify(self):
        self._write_command(CMD_BIT_MODIFY)
        self._wait_for_command(CMD_BIT_MODIFY)
        raise NotImplementedError

    def reset(self):
        self._write_command(CMD_RESET)
        raise NotImplementedError
    
    def read_status(self):
        self._write_command(CMD_READ_STATUS)
        self._wait_for_command(CMD_READ_STATUS)
        raise NotImplementedError

    def read(self):
        self._write_command(CMD_READ)
        self._wait_for_command(CMD_READ)
    
    def write(self):
        self._write_command(CMD_WRITE)
        raise NotImplementedError
    
    def check_message(self):
        self._write_command(CMD_CHECK_MESSAGE)
        self._wait_for_command(CMD_CHECK_MESSAGE)
        raise NotImplementedError
