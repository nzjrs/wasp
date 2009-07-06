#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import time
import os.path
import optparse
import ppz
import ppz.transport as transport
import ppz.communication as communication
import ppz.messages as messages

if __name__ == "__main__":
    thisdir = os.path.abspath(os.path.dirname(__file__))
    default_messages = os.path.join(thisdir, "..", "messages.xml")

    parser = optparse.OptionParser()
    ppz.setup_comm_optparse_options(parser, default_messages)

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
    s = communication.SerialCommunication(port=options.port, speed=options.speed, timeout=options.timeout)
    t = transport.Transport(check_crc=options.crc, debug=options.debug)

    s.connect_to_port()
    m.parse()

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
