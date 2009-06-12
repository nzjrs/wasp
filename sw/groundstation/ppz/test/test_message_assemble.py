import os.path

import testsetup
import ppz.messages as messages
import ppz.transport as transport

path = testsetup.get_messages()
i = messages.MessagesFile(xmlfile=path, debug=True)
i.parse()

m = i.get_message_by_name("TEST_MESSAGE")
assert m != None

t = transport.Transport(check_crc=True, debug=True)

data = t.pack_one(
            transport.TransportHeaderFooter(acid=0x78), 
            m,
            m.pack_values(1, -1, 10, -10, 100, -100, 1.0))

print data

m = i.get_message_by_name("PONG")
assert m != None

data = t.pack_one(
            transport.TransportHeaderFooter(acid=0x78), 
            m,
            m.pack_values())

