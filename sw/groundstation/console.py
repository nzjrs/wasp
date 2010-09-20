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

import gs
import gs.source as source
import gs.config as config

def message_received(comm, msg, header, payload):
    print msg
    if msg.size:
        print "\t", msg.unpack_printable_values(payload, joiner=",")

def uav_connected(source, connected):
    print "Source connected: %s" % connected

if __name__ == "__main__":
    parser = gs.get_default_command_line_parser(True, False, True, preferences_name="console.ini")
    options, args = parser.parse_args()

    m = messages.MessagesFile(path=options.messages, debug=options.debug)
    m.parse()

    c = config.Config(filename=options.preferences)

    s = source.UAVSource(c, m, options)
    s.connect("source-connected", uav_connected)
    s.communication.connect("message-received", message_received)

    s.connect_to_uav()
    gobject.MainLoop().run()

