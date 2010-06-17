#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
import sys
import gobject
import socket

import gs

import wasp.messages as messages
import wasp.communication as communication
import wasp.transport as transport

TEST_UAV_ACID_BASE = 0x50

class UAV:
    def __init__(self, i, options):

        self.messages = messages.MessagesFile(path=options.messages, debug=options.debug)
        self.messages.parse()

        self.transport = transport.Transport(check_crc=True, debug=options.debug)
        self.header = transport.TransportHeaderFooter(acid=i+TEST_UAV_ACID_BASE)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect( (options.groundstation_host, int(options.groundstation_port)) )

        self.dummy_uav = communication.DummyUAV(self.messages, self.send_message,
                disable_time=True,
                disable_comm=True,
                disable_imu=True,
                disable_status=True,
                disable_ppm=True,
                disable_ahrs=True,
                disable_gps=False,
                start_gps_lat=-43.520451+i
        )

    def send_message(self, msg, values):
        data = self.transport.pack_message_with_values(
                    self.header,
                    msg,
                    *values)

        try:
            l = self.sock.send(data)
            if l != len(data):
                print "Not all data sent: %d != %d" % (l, len(data))
        except socket.error, e:
            print "Send error: %s" % e


if __name__ == "__main__":
    parser = gs.get_default_command_line_parser(False, False, False)
    parser.add_option("--num-uavs",
                    default="2", metavar="2",
                    help="Number of UAVs to simulate")
    parser.add_option("--groundstation-host",
                    default="127.0.0.1", metavar="IP ADDRESS",
                    help="IP Address of Groundstation")
    parser.add_option("--groundstation-port",
                    default=str(communication.UDP_PORT), metavar="IP PORT",
                    help="IP Port of Groundstation")

    options, args = parser.parse_args()

    uavs = [UAV(int(i), options) for i in range(int(options.num_uavs))]
    gobject.MainLoop().run()

    sys.exit(1)



