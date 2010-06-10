#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import time
import os.path
import optparse
import gobject
import wasp
import wasp.transport as transport
import wasp.communication as communication
import wasp.messages as messages

def message_received(msg, header, payload):
    pass

def send_ping():
    pass

if __name__ == "__main__":
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "..", "onboard", "config", "messages.xml")

    parser = optparse.OptionParser()
    parser.add_option("-m", "--messages",
                    default=default_messages,
                    help="messages xml file", metavar="FILE")
    parser.add_option("-p", "--port",
                    default="/dev/ttyUSB0",
                    help="serial port")
    parser.add_option("-s", "--speed",
                    type="int", default=57600,
                    help="serial port baud rate")
    parser.add_option("-t", "--timeout",
                    type="int", default=1,
                    help="serial timeout")
    parser.add_option("-d", "--debug",
                    action="store_true",
                    help="print extra debugging information")
    parser.add_option("-c", "--crc",
                    action="store_true",
                    help="check message crc")
    parser.add_option("-q", "--quiet",
                    action="store_true",
                    help="do not print messages, useful with --debug")
    parser.add_option("-g", "--ping",
                    type="int", default=0,
                    help="send ping every n seconds, 0 disables [default]")

    options, args = parser.parse_args()

    m = messages.MessagesFile(path=options.messages, debug=options.debug)
    m.parse()
    t = transport.Transport(check_crc=options.crc, debug=options.debug)
    s = communication.Serial(t,m,wasp.transport.TransportHeaderFooter(acid=wasp.ACID_GROUNDSTATION))
    s.configure_connection(port=options.port,speed=options.speed,timeout=options.timeout)
    s.connect_to_port()

    t1 = t2 = time.time()
    while s.is_open():
        try:
            data = s.read()
            for header, payload in t.parse_many(data):
                msg = m.get_message_by_id(header.msgid)

                if not options.quiet:
                    print "%s\n\t" % msg,
                    print msg.unpack_printable_values(payload, joiner=",")

                t2 = time.time()
                if options.ping and (t2 - t1) > options.ping:
                    t1 = t2
                    p = m.get_message_by_name("PING")
                    data = t.pack_one(
                                transport.TransportHeaderFooter(acid=0x78), 
                                p,
                                p.pack_values())
                    s.write(data.tostring())

        except KeyboardInterrupt:
            s.disconnect_from_port()
            break
