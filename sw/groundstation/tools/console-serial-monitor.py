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

def message_received(comm, msg, header, payload, quiet):
    print msg
    if not quiet:
        if msg.size:
            print "\t", msg.unpack_printable_values(payload, joiner=",")

def uav_connected(comm, connected):
    print "Connected: %s" % connected

def send_ping(comm, msg):
    comm.send_message(msg, ())
    return True

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
    s = communication.SerialCommunication(t,m,wasp.transport.TransportHeaderFooter(acid=wasp.ACID_GROUNDSTATION))
    s.configure_connection(serial_port=options.port,serial_speed=options.speed,serial_timeout=options.timeout)

    s.connect("message-received", message_received, options.quiet)
    s.connect("uav-connected", uav_connected)

    if options.ping > 0:
        gobject.timeout_add(int(options.ping)*1000, send_ping, s, m.get_message_by_name("PING"))

    s.connect_to_uav()
    gobject.MainLoop().run()

