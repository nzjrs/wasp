import sqlite3
import time
import logging
import datetime
import gobject

import libserial

import gs
import gs.config
import gs.utils as utils

import wasp
import wasp.transport as transport
import wasp.communication as communication
import wasp.ui.treeview as treeview

DEBUG=False
LOG = logging.getLogger('uavsource')

class MessageCb:
    def __init__(self, cb, max_freq, **kwargs):
        self.cb = cb
        self.max_freq = max_freq
        self.kwargs = kwargs
        self.listen_acid = None

        if max_freq > 0:
            self._dt = 1.0/max_freq
            self._lastt = datetime.datetime.now()

    def call_cb(self, msg, header, payload, time):
        if self.max_freq <= 0:
            try:
                self.cb(msg, header, payload, **self.kwargs)
            except:
                LOG.warn("Error calling callback for %s" % msg, exc_info=True)
        else:
            self._lastt, enough_time_passed, dt = utils.has_elapsed_time_passed(
                                            then=self._lastt,
                                            now=time,
                                            dt=self._dt)
            if enough_time_passed:
                try:
                    self.cb(msg, header, payload, **self.kwargs)
                except Exception:
                    LOG.warn("Error calling callback for %s" % msg, exc_info=True)

    def for_selected_uav(self, acid):
        return self.listen_acid != None and (self.listen_acid == acid or self.listen_acid == wasp.ACID_ALL)

    def select_uav(self, acid):
        """
        Sets that this message should be called for UAVs with the given acid.
        Overrides any values set in :func:`gs.source.UAVSource.select_uav`
        """
        self.listen_acid = acid

    def quit(self):
        pass

class _LogSqliteCb(MessageCb):
    def __init__(self, logfile):
        if not logfile:
            logfile = gs.user_file_path("flight.sqlite")

        self._con = sqlite3.connect(
                        logfile,
                        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #by setting the text_factory as str, sqlite will not get in the way
        #when storing 8-bit bytestrings (i.e. the raw payload data)
        self._con.text_factory = str
        self._cur = self._con.cursor()
        self._cur.execute("CREATE TABLE data(time timestamp, acid INTEGER, msgid INTEGER, payload BLOB)")

    def call_cb(self, msg, header, payload, msgtime):
        self._cur.execute("INSERT INTO data(time, acid, msgid, payload) VALUES (?, ?, ?, ?)", (
                    msgtime,
                    int(header.acid),
                    int(header.msgid),
                    payload))

    def quit(self):
        if self._con and self._cur:
            #careful not to close the DB twice
            self._cur.close()
            self._con.close()
            self._con = self._cur = None

class _LogCsvCb(MessageCb):
    def __init__(self, logfile, msg):
        if not logfile:
            logfile = gs.user_file_path(msg.name + ".csv")
        self._f = open(logfile, 'w')

        #print the CSV header
        header = ["time", "acid"] + [f.name for f in msg.fields]
        self._f.write(", ".join(header)+"\n")

    def call_cb(self, msg, header, payload, msgtime):
        self._f.write("%f, %s, " % (
                time.mktime(msgtime.timetuple()) + msgtime.microsecond / 1e6,
                header.acid))
        self._f.write(
                msg.unpack_printable_values(payload, joiner=", "))
        self._f.write("\n")

    def quit(self):
        self._f.close()

class _SourceConfig:

    @staticmethod
    def get_preference_widgets(configurable):
        return None, None, []

class _SourceConfigSerial(_SourceConfig):

    @staticmethod
    def get_preference_widgets(configurable):
        self = configurable
        sg = self.build_sizegroup()
        ser_port_cb = self.build_combo("serial_port", *libserial.get_ports())
        ser_speed_cb = self.build_combo("serial_speed", *libserial.get_speeds())
        items = [ser_port_cb, ser_speed_cb]
        frame = self.build_frame(None, [
            self.build_label("Serial Port", ser_port_cb, sg=sg),
            self.build_label("Serial Baud", ser_speed_cb, sg=sg),
        ])
        return "UAV Source", frame, items

_SOURCE_CONFIG_GUIS = {
    communication.SerialCommunication.COMMUNICATION_TYPE : _SourceConfigSerial
}

class UAVSource(gs.config.ConfigurableIface, gobject.GObject):

    CONFIG_SECTION = "UAVSOURCE"

    DEFAULT_TIMEOUT = 1

    #: the groundstation is (physically) connected to the UAV
    STATUS_CONNECTED                =   1
    #: the groundstation is connected and receiving data
    STATUS_CONNECTED_LINK_OK        =   2
    #: the groundstation is disconnected from the UAV
    STATUS_DISCONNECTED             =   3

    __gsignals__ = {
            "source-connected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
                gobject.TYPE_BOOLEAN]),     #True if source connected
            "source-link-status-change" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
                gobject.TYPE_BOOLEAN]),     #True if recieving data
            "uav-detected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
                gobject.TYPE_INT]),         #The ACID of a detected UAV
            "uav-selected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
                gobject.TYPE_INT]),         #The ACID of a selected UAV
    }

    def __init__(self, conf, messages, options, listen_acid=wasp.ACID_ALL):
        gs.config.ConfigurableIface.__init__(self, conf)
        gobject.GObject.__init__(self)

        self._rxts = treeview.MessageTreeStore()

        #dictionary of msgid : [list, of, MessageCb objects]
        self._callbacks = {}

        #for tracking UAVs we have seen and are communicating with
        self._listen_acid = listen_acid
        self._desination_acid = wasp.ACID_ALL
        self._seen_acids = {}

        self._messages_file = messages
        self._transport = transport.Transport(check_crc=True, debug=DEBUG)
        self._groundstation_header = wasp.transport.TransportHeaderFooter(acid=wasp.ACID_GROUNDSTATION)
        self._rm = self._messages_file.get_message_by_name("REQUEST_MESSAGE")
        self._rt = self._messages_file.get_message_by_name("REQUEST_TELEMETRY")

        source_name, comm_klass, cmdline_config = communication.get_source(options.source)
        LOG.info("Source: %s" % comm_klass)
        self.communication = comm_klass(self._transport, self._messages_file, self._groundstation_header)

        #configure the class, updating with command line values
        self._default_config = self.communication.get_configuration_default()
        self._default_config.update(cmdline_config)
        self.communication.configure_connection(**self._default_config)
        LOG.debug("Source config: %s" % self._default_config)

        #attach the config UI
        self._config_gui = _SOURCE_CONFIG_GUIS.get(source_name, _SourceConfig)()

        self.communication.connect("message-received", self.on_message_received)
        self.communication.connect("uav-connected", self.on_uav_connected)

        #track how many messages per second
        self._linkok = False
        self._linktimeout = datetime.timedelta(seconds=2)
        self._lastt = datetime.datetime.now()
        self._times = utils.MovingAverage(5, float)
        gobject.timeout_add(2000, self._check_link_status)

        #track the ping time
        self._sendping = None
        self._pingtime = 0
        self._pingmsg = messages.get_message_by_name("PING")
        self.register_interest(self._got_pong, 0, "PONG")
        if options.ping_time > 0:
            gobject.timeout_add(1000*options.ping_time, self._do_ping)

    def _got_pong(self, msg, header, payload):
        #calculate difference in send and rx in milliseconds
        self._pingtime = utils.calculate_dt_seconds(self._sendping, datetime.datetime.now())
        self._pingtime *= 1000.0

    def _do_ping(self):
        self._sendping = datetime.datetime.now()
        self.send_message(self._pingmsg, ())
        return True

    def _check_link_status(self):
        ok = (datetime.datetime.now() - self._lastt) < self._linktimeout
        if ok != self._linkok:
            self._linkok = ok
            self.emit("source-link-status-change", self._linkok)
        return True

    def _save_callback(self, msg, mcb):
        try:
            self._callbacks[msg.id].append(mcb)
        except KeyError:
            self._callbacks[msg.id] = [mcb]

    def _message_for_selected_uav(self, acid):
        return self._listen_acid == wasp.ACID_ALL or self._listen_acid == acid 

    def select_uav(self, acid):
        """ Sets that we should only listen for messages from UAVs with the given acid """
        self._listen_acid = acid
        self.emit("uav-selected", acid)

    def get_selected_uav(self):
        """ Returns the UAV that we are listening for messages from """
        return self._listen_acid

    def get_status(self):
        """ Returns the connection status, :const:`gs.source.UAVSource.STATUS_CONNECTED` etc """
        if self.communication.is_connected():
            if self._linkok:
                return self.STATUS_CONNECTED_LINK_OK
            return self.STATUS_CONNECTED
        return self.STATUS_DISCONNECTED

    def register_csv_logger(self, logfilepath, *message_names):
        """ Registers messages to be logged to a CSV file """
        #only allowed one CSV per message
        for m in message_names:
            msg = self._messages_file.get_message_by_name(m)
            if not msg:
                LOG.critical("Unknown message: %s" % m)

            mcb = _LogCsvCb(logfilepath, msg)
            self._save_callback(msg, mcb)

    def register_sqlite_logger(self, logfilepath, *message_names):
        """ Registers messages to be logged to a sqlite database """
        #the sqlite logger can store multiple messages in the same DB
        mcb = _LogSqliteCb(logfilepath)
        for m in message_names:
            msg = self._messages_file.get_message_by_name(m)
            if not msg:
                LOG.critical("Unknown message: %s" % m)

            self._save_callback(msg, mcb)

    def register_interest(self, cb, max_frequency, *message_names, **user_data):
        """
        Register interest in receiving a callback when a message with the specified 
        name arrives.

        :param cb: a callback to be called. The signature is (msg, header, payload, \*\*user_data)
        :param max_frequency: the max frequency to receive callbacks
        :param message_names: a list of message names to watch for
        :returns: a list of :class:`gs.source.MessageCb` objects
        """
        mcbs = []
        for m in message_names:
            msg = self._messages_file.get_message_by_name(m)
            if not msg:
                LOG.critical("Unknown message: %s" % m)

            mcb = MessageCb(cb, max_frequency, **user_data)
            mcbs.append(mcb)
            self._save_callback(msg, mcb)
        return mcbs

    def unregister_interest(self, cb):
        """
        Unregisters a previously registered (using :func:`gs.source.UAVSource.register_interest`) callback
        """
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

    def on_uav_connected(self, communication, connected):
        self.emit("source-connected", connected)

    def on_message_received(self, communication, msg, header, payload):
        time = datetime.datetime.now()
        acid = header.acid

        for cb in self._callbacks.get(msg.id, ()):
            if self._message_for_selected_uav(acid) or cb.for_selected_uav(acid):
                cb.call_cb(msg, header, payload, time)

        if self._message_for_selected_uav(acid):
            self._rxts.update_message(msg, payload)
            self._times.add(utils.calculate_dt_seconds(self._lastt, time))
            self._lastt = time

        if acid not in self._seen_acids:
            self._seen_acids[acid] = True
            self.emit("uav-detected", acid)


    def get_rx_message_treestore(self):
        """ Returns the gtk.TreeStore that holds recieved message details """
        return self._rxts

    def send_message(self, msg, values):
        """ Sends a message to the UAV """
        if self.communication.is_connected():
            #FIXME: pass the header in here
            self.communication.send_message(msg, values)

    def connect_to_uav(self):
        """ Connects the communication to the UAV """
        self.communication.connect_to_uav()

    def disconnect_from_uav(self):
        """ Disconnects the communication from the UAV """
        self.communication.disconnect_from_uav()

    def refresh_uav_info(self):
        """ Requests information about the UAV, from the BUILD_INFO message """
        m = self._messages_file.get_message_by_name("BUILD_INFO")
        self.request_message(m.id)

    def request_message(self, message_id):
        """ Resuests the UAV send us the message with the supplied ID """
        self.send_message(self._rm, (message_id,))

    def request_telemetry(self, message_name, frequency):
        """
        Requests the UAV send us telementry, i.e. the supplied *message_name*
        at the supplied *frequency*
        """
        frequency = float(frequency)
        LOG.info("Requesting telemetry: %s @ %.1fHz" % (message_name, frequency))
        m = self._messages_file.get_message_by_name(message_name)
        self.send_message(self._rt, (m.id, frequency))

    def stop_telemetry(self, message_name):
        """
        Tells the UAV to stop sending us telemetry of the supplied *message_name*
        """
        LOG.info("Stopping telemetry %s" % message_name)
        self.request_telemetry(message_name, 0.0);

    def quit(self):
        """ Cleans up all resources, disconnects callbacks, etc """
        self.disconnect_from_uav()
        for cbs in self._callbacks.values():
            for cb in cbs:
                cb.quit()

    def get_connection_parameters(self):
        """
        Returns a 2-tuple, the name of the connection, and a string describing
        its configuration
        """
        return self.communication.COMMUNICATION_TYPE, self.communication.get_connection_string()

    def get_messages_per_second(self):
        """ Returns the number of messages received from the UAV per second """
        if self._linkok:
            try:
                return 1.0/self._times.average()
            except ZeroDivisionError:
                pass
        return 0.0

    def get_ping_time(self):
        """ Returns the average round trip time to ping the UAV """
        if self._linkok:
            if self._sendping:
                return self._pingtime
        return 0.0

    def update_state_from_config(self):
        for k in self._default_config:
            if self.config_has_key(k):
                self._default_config[k] = self.config_get(k, default=self._default_config[k])

    def update_config_from_state(self):
        for k in self._default_config:
            self.config_set(k, self._default_config[k])

    def get_preference_widgets(self):
        return self._config_gui.get_preference_widgets(self)




