from pynq.iop.arduino_can_bus import Can,Message
import constants

class OBD:

    def __init__(self):
        self.can = Can()

    def ecu_req(self, pid):
        message = Message()
        message.id = constants.PID_REQUEST
        message.rtr = 0
        message.length = 8
        message.data = [
            [2, 1, pid, 0],
            [0, 0, 0, 0]
        ]

        self.can.bit_modify(constants.CANCTRL, int('0b11100000', 2), 0)

        self.can.send_message(message)

        message = self.can.get_message()
        if message.data[0][2] == constants.ENGINE_RPM:
            print("Engine RPM: ")
            engine_data = ((message.data[0][3]*256) + message.data[1][0])/4
        elif message.data[0][2] == constants.ENGINE_COOLANT_TEMP:
            print("Engine Coolant Temp (C): ")
            engine_data = message.data[0][3] - 40
        elif message.data[0][2] == constants.VEHICLE_SPEED:
            print("Vehicle Speed: ")
            engine_data = message.data[0][3]
        elif message.data[0][2] == constants.MAF_SENSOR:
            print("MAF Status: " )
            engine_data = ((message.data[0][3]*256) + message.data[1][0])/100
        elif message.data[0][2] == constants.THROTTLE:
            print("THROTTLE: ")
            engine_data = (message.data[0][3]*100)/255;
        else:
            engine_data = "Invalid PID detected"
        print(engine_data)
