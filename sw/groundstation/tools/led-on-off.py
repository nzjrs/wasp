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
    if connected:
        global led, led_cmd
        msg = msgs.get_message_by_name("GPIO_%s" % led_cmd)
        cmd.send_command(msg, (led,), cmd_ok, cmd_fail)
        name, config = src.get_connection_parameters()
        print "%s connected: %s" % (name, config)
    else:
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
    source = source.UAVSource(c, m, options)
    cmd = fms.CommandManager(source.communication)
    source.connect("source-connected", uav_connected, m, cmd)
    source.connect_to_uav()

    global loop
    loop = gobject.MainLoop()
    loop.run()

