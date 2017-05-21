from pynq.iop.arduino_can_bus import Can,Message

message = Message()
message.data = [[1,2,3,4],[5,6,7,8]]

c = Can()
c._write_message(message)
print(message)
data = c._read_message()
print(data)