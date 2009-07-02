import logging

import libserial

import gs.config as config

import ppz
import ppz.transport as transport
import ppz.messages as messages
import ppz.monitor as monitor

DEBUG=False
LOG = logging.getLogger('uavsource')

class _Source:
    def register_intrest(self, *messages, **user_data):
        raise NotImplementedError

class UAVSource(monitor.GObjectSerialMonitor, _Source, config.ConfigurableIface):

    CONFIG_SECTION = "UAVSOURCE"

    DEFAULT_PORT = "/dev/ttyUSB0"
    DEFAULT_SPEED = 57600
    DEFAULT_TIMEOUT = 1

    def __init__(self, conf):
        self._serialsender = transport.SerialTransport(port="/dev/ttyUSB0", speed=57600, timeout=1)
        monitor.GObjectSerialMonitor.__init__(self, self._serialsender)

        config.ConfigurableIface.__init__(self, conf)

        self._transport = transport.Transport(check_crc=True, debug=DEBUG)
        self._messages_file = messages.MessagesFile(path="/home/john/Programming/wasp.git/sw/messages.xml", debug=DEBUG)
        self._messages_file.parse()

        self._port = None
        self._speed = None

    def on_serial_data_available(self, fd, condition, serial):

        data = serial.read(1)
        for header, payload in self._transport.parse_many(data):
            msg = self._messages_file.get_message_by_id(header.msgid)
            if msg:
                print msg
            #    self._rxts.update_message(msg, payload)

        return True

    def quit(self):
        self.disconnect_from_uav()

    def connect_to_uav(self):
        if self._port and self._speed:
            self._serialsender.connect_to_port()

    def disconnect_from_uav(self):
        self._serialsender.disconnect_from_port()

    def update_state_from_config(self):
        self._port = self.config_get("serial_port", self.DEFAULT_PORT)
        self._speed = self.config_get("serial_speed", self.DEFAULT_SPEED)
        LOG.info("Updating state from config: %s %s" % (self._port, self._speed))
        #if p:
        #    self.connect(port=p)

    def update_config_from_state(self):
        LOG.info("Updating config from state")
        self.config_set("serial_port", self._port or self.DEFAULT_PORT)
        self.config_set("serial_speed", self._speed or self.DEFAULT_SPEED)

    def get_preference_widgets(self):
        ser_port_cb = self.build_combo("serial_port", *libserial.get_ports())
        ser_speed_cb = self.build_combo("serial_speed", *libserial.get_speeds())

        #all following items configuration is saved
        items = [ser_port_cb, ser_speed_cb]

        #the gui looks like
        sg = self.make_sizegroup()
        frame = self.build_frame(None, [
            self.build_label("Serial Port", ser_port_cb, sg),
            self.build_label("Serial Baud", ser_speed_cb, sg),
        ])

        return "UAV Source", frame, items


