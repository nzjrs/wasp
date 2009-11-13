import logging
import datetime
import gobject

import libserial

import gs.config as config
import gs.utils as utils

import wasp
import wasp.transport as transport
import wasp.communication as communication
import wasp.messages as messages
import wasp.monitor as monitor
import wasp.ui.treeview as treeview

DEBUG=False
LOG = logging.getLogger('uavsource')

class _MessageCb:
    def __init__(self, cb, max_freq, **kwargs):
        self.cb = cb
        self.max_freq = max_freq
        self.kwargs = kwargs

        if max_freq > 0:
            self._dt = 1.0/max_freq
            self._lastt = datetime.datetime.now()

    def call_cb(self, msg, payload, time):
        if self.max_freq <= 0:
            self.cb(msg, payload, **self.kwargs)
        else:
            self._lastt, enough_time_passed, dt = utils.has_elapsed_time_passed(
                                            then=self._lastt,
                                            now=time,
                                            dt=self._dt)
            if enough_time_passed:
                try:
                    self.cb(msg, payload, **self.kwargs)
                except Exception:
                    LOG.warn("Error calling callback for %s" % msg, exc_info=True)

class UAVSource(monitor.GObjectSerialMonitor, config.ConfigurableIface):

    CONFIG_SECTION = "UAVSOURCE"

    DEFAULT_PORT = "/dev/ttyUSB0"
    DEFAULT_SPEED = 57600
    DEFAULT_TIMEOUT = 1

    PING_TIME = 3

    def __init__(self, conf, messages, source_name, **source_options):
        config.ConfigurableIface.__init__(self, conf)

        self._port = self.config_get("serial_port", self.DEFAULT_PORT)
        self._speed = self.config_get("serial_speed", self.DEFAULT_SPEED)
        self._rxts = None

        #dictionary of msgid : [list, of, _MessageCb objects]
        self._callbacks = {}

        self._messages_file = messages
        self._rm = self._messages_file.get_message_by_name("REQUEST_MESSAGE")
        self._rt = self._messages_file.get_message_by_name("REQUEST_TELEMETRY")
        self._transport = transport.Transport(check_crc=True, debug=DEBUG)
        self._transport_header = transport.TransportHeaderFooter(acid=0x78)

        #set up the all the possible source options for all possible
        #communication sources. 

        #FIXME: Command line options override those that for serial port
        #should override those in config file
        sourceopts = {
            "serial_port"   :   self._port,
            "serial_speed"  :   int(self._speed),
            "serial_timeout":   1,
            "messages"      :   self._messages_file,
            "transport"     :   self._transport,
            "header"        :   self._transport_header,
            "fifo_path"     :   source_options.get("fifo_path"),
        }

        self.serial = communication.communication_factory(source_name, **sourceopts)
        self._use_test_source = source_name == "test"
        LOG.info("Source enabled: %s" % source_name)

        monitor.GObjectSerialMonitor.__init__(self, self.serial)

        #because we already initialized the base gobject type uising the
        #__signals__ defined in monitor.GObjectSerialMonitor, we must
        #programatically add the source-connected signal
        gobject.signal_new(
                'source-connected', UAVSource,
                gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                (bool,))

        #track how many messages per second
        self._lastt = datetime.datetime.now()
        self._times = utils.MovingAverage(5, float)

        #track the ping time
        self._sendping = None
        self._pingtime = 0
        self._pingmsg = messages.get_message_by_name("PING")
        self.register_interest(self._got_pong, 0, "PONG")
        gobject.timeout_add_seconds(2, self._do_ping)

    def _got_pong(self, msg, payload):
        #calculate difference in send and rx in milliseconds
        self._pingtime = utils.calculate_dt_seconds(self._sendping, datetime.datetime.now())
        self._pingtime *= 1000.0

    def _do_ping(self):
        self._sendping = datetime.datetime.now()
        self.send_message(self._pingmsg, ())
        return True

    def register_interest(self, cb, max_frequency, *message_names, **user_data):
        """
        Register interest in receiving a callback when a message with the specified 
        name arrives.

        @cb: Callback to be called. The signature is (msg, payload, **user_data)
        @max_frequency: Max frequency to receive callbacks
        @message_names: List of message names to watch for
        """
        for m in message_names:
            msg = self._messages_file.get_message_by_name(m)
            if not msg:
                LOG.critical("Unknown message: %s" % m)

            cb = _MessageCb(cb, max_frequency, **user_data)
            try:
                self._callbacks[msg.id].append(cb)
            except KeyError:
                self._callbacks[msg.id] = [cb]

    def unregister_interest(self, cb):
        fid = None
        fcb = None
        for msgid in self._callbacks:
            for mcb in self._callbacks[msgid]:
                if mcb.cb == cb:
                    mcb.cb = None
                    fid = msgid
                    fcb = mcb

        if fid and fcb:
            self._callbacks[fid].remove(fcb)

    def on_serial_data_available(self, fd, condition, serial):
        data = serial.read(1)
        for header, payload in self._transport.parse_many(data):
            msg = self._messages_file.get_message_by_id(header.msgid)
            if msg:
                time = datetime.datetime.now()
                cbs = self._callbacks.get(msg.id, ())
                for cb in cbs:
                    cb.call_cb(msg, payload, time)

                if self._rxts:
                    self._rxts.update_message(msg, payload)

                self._times.add(utils.calculate_dt_seconds(self._lastt, time))
                self._lastt = time

        return True

    def get_rx_message_treestore(self):
        if self._rxts == None:
            self._rxts = treeview.MessageTreeStore()
        return self._rxts

    def send_message(self, msg, values):
        if msg:
            data = self._transport.pack_message_with_values(
                        self._transport_header, 
                        msg,
                        *values)
            self.serial.write(data.tostring())

    def request_message(self, message_id):
        self.send_message(self._rm, (message_id,))

    def request_telemetry(self, message_name, frequency):
        m = self._messages_file.get_message_by_name(message_name)
        self.send_message(self._rt, (m.id, frequency))

    def quit(self):
        self.disconnect_from_uav()

    def get_connection_parameters(self):
        return self._port, self._speed

    def connect_to_uav(self):
        if self._port and self._speed:
            self.serial.connect_to_port()
        self.emit("source-connected", self.serial.is_open())

    def disconnect_from_uav(self):
        self.serial.disconnect_from_port()
        self.emit("source-connected", self.serial.is_open())

    def get_messages_per_second(self):
        try:
            return 1.0/self._times.average()
        except ZeroDivisionError:
            return 0.0

    def get_ping_time(self):
        if self._sendping:
            return self._pingtime
        else:
            return 0.0

    def update_state_from_config(self):
        port = self.config_get("serial_port", self.DEFAULT_PORT)
        speed = self.config_get("serial_speed", self.DEFAULT_SPEED)

        if port != self._port or speed != self._speed:
            if not self._use_test_source:
                if self.serial.is_open():
                    self.disconnect_from_uav()

                #instatiate the new source, and call change_serialsender
                #to reconnect to the underlying object signals telling us
                #when data has arrived
                LOG.info("Connecting to UAV on new port: %s %s" % (port, speed))
                self.serial = communication.SerialCommunication(port=port, speed=int(speed), timeout=1)
                self.change_serialsender(self.serial)

        self._port = port
        self._speed = speed
        LOG.info("Updating state from config: %s %s" % (self._port, self._speed))

    def update_config_from_state(self):
        LOG.info("Updating config from state")
        self.config_set("serial_port", self._port or self.DEFAULT_PORT)
        self.config_set("serial_speed", self._speed or self.DEFAULT_SPEED)

    def get_preference_widgets(self):
        sg = self.make_sizegroup()
        ser_port_cb = self.build_combo("serial_port", *libserial.get_ports(), sg=sg)
        ser_speed_cb = self.build_combo("serial_speed", *libserial.get_speeds(), sg=sg)

        #all following items configuration is saved
        items = [ser_port_cb, ser_speed_cb]

        #the gui looks like
        frame = self.build_frame(None, [
            self.build_label("Serial Port", ser_port_cb),
            self.build_label("Serial Baud", ser_speed_cb),
        ])

        return "UAV Source", frame, items


