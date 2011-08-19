#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import time
import sys
import os.path
import optparse
import gobject

try:
    import wasp
except ImportError:
    sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")))
    import wasp

import wasp.transport as transport
import wasp.communication as communication
import wasp.messages as messages
import wasp.fms as fms

import gs
import gs.source as source
import gs.config as config

def cmd_ok(cmd_id):
    global source
    print "CMD_OK"
    source.disconnect_from_uav()

def cmd_fail(*args):
    global source
    print "CMD_FAIL"
    source.disconnect_from_uav()

def uav_connected(src, connected, msgs, cmd):
    name, config = src.get_connection_parameters()
    if connected:
        global led, led_cmd
        msg = msgs.get_message_by_name("GPIO_%s" % led_cmd)
        cmd.send_command(msg, (led,), cmd_ok, cmd_fail)
        print "%s connected: %s" % (name, config)
    else:
        print "%s disconnected: %s" % (name, config)
        global loop
        loop.quit()

if __name__ == "__main__":
    parser = gs.get_default_command_line_parser(True, False, True, preferences_name="console.ini")
    options, args = parser.parse_args()

    global led, led_cmd
    led = 4
    led_cmd = "ON"
    try:
        led = int(args[1])
        led_cmd = args[0].upper()
    except:
        pass

    m = messages.MessagesFile(path=options.messages, debug=options.debug)
    m.parse()

    c = config.Config(filename=options.preferences)

    global source
    global loop

    loop = gobject.MainLoop()
    source = source.UAVSource(c, m, options)
    cmd = fms.CommandManager(source.communication)
    source.connect("source-connected", uav_connected, m, cmd)
    source.connect_to_uav()
    loop.run()

