import sys
import socket

import wasp.communication
import wasp.messages
import wasp.transport

TEST_ACID = 65

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    host = sys.argv[1]
except IndexError:
    host = "localhost"

print "connecting to %s" % host
sock.connect((host, wasp.communication.UDP_PORT))

mf = wasp.messages.MessagesFile(path="/home/john/Programming/wasp.git/sw/onboard/config/messages.xml", debug=False)
mf.parse()

transport = wasp.transport.Transport(check_crc=True, debug=False)
data = transport.pack_message_with_values(
            wasp.transport.TransportHeaderFooter(acid=TEST_ACID),
            mf.get_message_by_name("PING"))

l = sock.send(data)
print "sent %d/%d bytes" % (l, len(data))

sock.close()
