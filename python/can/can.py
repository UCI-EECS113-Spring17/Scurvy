from pynq.iop.arduino_io import Arduino_IO as IO

ARDUINO_IF_ID = 3

# SPI Port definitions
_MOSI = IO(ARDUINO_IF_ID,14,'out')
_MISO = IO(ARDUINO_IF_ID,15,'in')
_SCK = IO(ARDUINO_IF_ID,13,'out')
_CS = IO(ARDUINO_IF_ID,16,'out')

class Can {
    '''Object representing CAN protocol communication capabilities.'''

    def __init__(self):
        self.id = int()
        self.data = list(int)

    def write():
        raise NotImplementedError

    def read():
        raise NotImplementedError
}