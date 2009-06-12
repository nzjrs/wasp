#!/usr/bin/env python2.5

import optparse
import ppz.transport as transport
import ppz.messages as messages

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-m", "--messages",
                    default="/home/john/Programming/paparazzi.git/conf/messages.xml",
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

    options, args = parser.parse_args()

    m = messages.MessagesFile(xmlfile=options.messages, debug=options.debug)
    s = transport.SerialTransport(port=options.port, speed=options.speed, timeout=options.timeout)
    t = transport.Transport(check_crc=options.crc, debug=options.debug)

    s.connect_to_port()
    m.parse()

    i = 0
    while s.is_open():
        try:
            data = s.read()
            for header, payload in t.parse_many(data):
                msg = m.get_message_by_id(header.msgid)
                print "%s\n\t" % msg,
                print msg.unpack_printable_values(payload, joiner=",")

                if i == 10:
                    p = m.get_message_by_name("PONG")
                    data = t.pack_one(
                                transport.TransportHeaderFooter(acid=0x78), 
                                p,
                                p.pack_values())
                    s.write(data.tostring())
                    i = 0;
                i += 1

        except KeyboardInterrupt:
            s.disconnect_from_port()
            break
