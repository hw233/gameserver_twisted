from common.header import SimpleHeader
from common import  conf
import struct

class MsgTest(SimpleHeader):
    # notify clients load map
    def __init__(self, data):
        super(MsgTest, self).__init__(conf.MSG_SC_MAP_LOAD)
        self.append_param('seed', data, 's')



data = struct.pack("<ifi", 1,-1.23,1)
fin = struct.unpack('<ifi',data)

msg = MsgTest(data)

newdata = msg.marshal()

msg.unmarshal(newdata)

findata = msg.seed

fin = struct.unpack('<ifi',findata)

a = 1

from GameObject.MaterialObject import KKK

cell = KKK()
obj = cell.split(1)