from pynq import MMIO
from pynq.iop import request_iop
from pynq.iop import iop_const
from pynq.iop import Arduino_IO

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

class Can(Object):
    '''Object representing pure IOP communication.'''

    def __init__(self, if_id: int):
        self.iop = request_iop(if_id, CAN_BUS_BIN)
        self.mmio = self.iop.mmio
        self.iop.start()

    def _write_command(self, cmd: int):
        self.mmio.write(iop_const.MAILBOX_OFFSET +
            iop_const.MAILBOX_PY2IOP_CMD_OFFSET, cmd)

    def _wait_for_command(self, cmd: int):
        while(self.mmio.read(
                iop_const.MAILBOX_OFFSET+
                iop_const.MAILBOX_PY2IOP_CMD_OFFSET) == cmd):
            pass

    def send_message(self):
        self._write_command(CMD_SEND_MESSAGE)
        raise NotImplementedError

    def get_message(self):
        self._write_command(CMD_GET_MESSAGE)
        self._wait_for_command(CMD_GET_MESSAGE)
        raise NotImplementedError
    
    def bit_modify():
        self._write_command(CMD_BIT_MODIFY)
        self._wait_for_command(CMD_BIT_MODIFY)
        raise NotImplementedError

    def reset():
        self._write_command(CMD_RESET)
        raise NotImplementedError
    
    def read_status():
        self._write_command(CMD_READ_STATUS)
        self._wait_for_command(CMD_READ_STATUS)
        raise NotImplementedError

    def read():
        self._write_command(CMD_READ)
        self._wait_for_command(CMD_READ)
        raise NotImplementedError
    
    def write():
        self._write_command(CMD_WRITE)
        raise NotImplementedError
    
    def check_message():
        self._write_command(CMD_CHECK_MESSAGE)
        self._wait_for_command(CMD_CHECK_MESSAGE)
        raise NotImplementedError
