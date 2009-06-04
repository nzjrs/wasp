import os.path

import testsetup
import ppz.transport as transport
import ppz.messages as messages

data = open(os.path.join(testsetup.TEST_DIR,"capture.dat")).read()
path = "/home/john/UAV/paparazzi3/conf/messages.xml"

t = transport.TransportParser(check_crc=False, debug=False)
m = messages.MessagesFile(path)
m.parse(debug=True)

for payload in t.parse_many(data):
    acid = ord(payload[0])
    mid = ord(payload[1])
    
    msg = m.get_message_by_id(mid)
    #print msg.get_values(payload[2:])
    print msg.get_all_printable_values(payload[2:], joiner=",")
            


