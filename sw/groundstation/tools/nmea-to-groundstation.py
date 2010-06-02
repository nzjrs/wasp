#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
import sys
import gobject
import socket

import gs
import gs.NMEA as NMEA

import wasp.messages as messages
import wasp.communication as communication
import wasp.transport as transport

import libserial.SerialSender as serialsender

TEST_ACID = 65

class Bridge:
    def __init__(self, options):

        self.line = ""
        self.watch = None

        self.messages = messages.MessagesFile(path=options.messages, debug=options.debug)
        self.messages.parse()
        self.msg_vtg = self.messages.get_message_by_name("GPS_VTG")
        self.msg_llh = self.messages.get_message_by_name("GPS_LLH")
        self.msg_gsv = self.messages.get_message_by_name("GPS_GSV")

        self.transport = transport.Transport(check_crc=True, debug=options.debug)
        self.header = transport.TransportHeaderFooter(acid=TEST_ACID)

        self.NMEA = NMEA.NMEA()

        self.serialsender = serialsender.SerialSender(port=options.serial_port, speed=int(options.serial_speed))
        self.serialsender.connect("serial-connected", self.on_serial_connected)
        self.serialsender.connect_to_port()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect( (options.groundstation_host, int(options.groundstation_port)) )

    def on_serial_connected(self, sender, connected):
        #remove the old watch
        if self.watch:
            gobject.source_remove(self.watch)

        if connected:
            #add new watch
            self.watch = gobject.io_add_watch(
                            self.serialsender.get_fd(),
                            gobject.IO_IN | gobject.IO_PRI,
                            self.on_serial_data_available,
                            self.serialsender.get_serial(),
                            priority=gobject.PRIORITY_HIGH
            )

    def send_vtg(self):
        data = self.transport.pack_message_with_values(
                        self.header,
                        self.msg_vtg,
                        self.NMEA.vtg_track,
                        self.NMEA.vtg_speed)
        l = self.sock.send(data)
        if l != len(data):
            raise Exception("Not all data sent: %d != %d" % (l, len(data)))

#   <message name="GPS_GSV" id="42">
#      <field name="sv"  type="uint8"/>
#      <field name="id"  type="uint8"/>
#      <field name="elevation"  type="uint16"/>
#      <field name="aximuth"  type="uint16"/>
#      <field name="snr"  type="uint8"/>
#   </message>
    def send_sat(self, i):
        data = self.transport.pack_message_with_values(
                        self.header,
                        self.msg_gsv,
                        self.NMEA.in_view,
                        self.NMEA.prn[i],
                        self.NMEA.elevation[i],
                        self.NMEA.azimuth[i],
                        self.NMEA.ss[i])
        l = self.sock.send(data)
        if l != len(data):
            raise Exception("Not all data sent: %d != %d" % (l, len(data)))

    def send_gsv(self):
        #send all 
        for i in range(0,self.NMEA.in_view):
            self.send_sat(i)

#   <message name="GPS_LLH" id="36">
#      <field name="fix" type="uint8" values="NONE|2D|3D"/>
#      <field name="sv" type="uint8"/>
#      <!-- scale value of 1e7 taken from ublox datasheet -->
#      <field name="lat"  type="int32" alt_unit_coef="1e-7"/> 
#      <field name="lon"  type="int32" alt_unit_coef="1e-7"/>
#      <field name="hsl"  type="int32" unit="mm"/>
#      <field name="hacc"  type="int32" unit="mm"/>
#      <field name="vacc"  type="int32" unit="mm"/>
#   </message>
    def send_llh(self):
        lat = int(self.NMEA.lat * 1e7)
        lon = int(self.NMEA.lon * 1e7)
        alt = int(self.NMEA.altitude * 1000.0) #m -> mm

        data = self.transport.pack_message_with_values(
                        self.header,
                        self.msg_llh,
                        2,
                        self.NMEA.satellites,
                        lat,
                        lon,
                        alt,
                        1,
                        1)
        l = self.sock.send(data)
        if l != len(data):
            raise Exception("Not all data sent: %d != %d" % (l, len(data)))

    def on_serial_data_available(self, fd, condition, serial):
        data = serial.read(1)
        self.line += data
        if data == "\n":
            ok = self.NMEA.handle_line(self.line)
            if ok == self.NMEA.OK:
                last_message = self.NMEA.last_message
                verb = "Got"
                if last_message == "GPVTG":
                    self.send_vtg()
                    verb = "Sent"
                elif last_message == "GPGSV":
                    self.send_gsv()
                    verb = "Sent"
                elif last_message == "GPGGA":
                    self.send_llh()
                    verb = "Sent"

                print "%s Message: %s" % (verb, last_message)
            else:
                print ok
            self.line = ""
        return True

if __name__ == "__main__":
    parser = gs.get_default_command_line_parser(False, False, False)
    parser.add_option("--serial-port",
                    default="/dev/ttyUSB1", metavar="/dev/ttyUSBn",
                    help="Serial port of GPS receiver")
    parser.add_option("--serial-speed",
                    default="9600", metavar="9600",
                    help="Serial baud of GPS receiver")
    parser.add_option("--groundstation-host",
                    default="127.0.0.1", metavar="IP ADDRESS",
                    help="IP Address of Groundstation")
    parser.add_option("--groundstation-port",
                    default=str(communication.UDP_PORT), metavar="IP PORT",
                    help="IP Port of Groundstation")

    options, args = parser.parse_args()

    Bridge(options)
    gobject.MainLoop().run()

    sys.exit(1)



