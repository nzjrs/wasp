import os.path
import socket
import random
import gobject
import logging

import libserial.SerialSender

import wasp
import wasp.transport
import wasp.fms

UDP_PORT = 1212

LOG = logging.getLogger('wasp.communication')

class _Communication(gobject.GObject):

    COMMUNICATION_TYPE = ""

    __gsignals__ = {
        "message-received" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT,      #message
            gobject.TYPE_PYOBJECT,      #header
            gobject.TYPE_PYOBJECT]),    #payload
        "uav-connected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_BOOLEAN]),     #true if successfully connected to UAV
    }

    def __init__(self, transport, messages_file, message_header, *args, **kwargs):
        gobject.GObject.__init__(self)
        self.transport = transport
        self.messages_file = messages_file
        self.message_header = message_header

    def send_message(self, msg, values):
        """
        Sends the supplied message to the UAV

        :param msg: a :class:`wasp.messages.Message` object
        :param values: a tuple/list of values for the message
        """
        pass

    def connect_to_uav(self):
        pass

    def disconnect_from_uav(self):
        pass

    def is_connected(self):
        pass

    def configure_connection(self, **kwargs):
        pass

    def get_configuration_default(self):
        return {}

    @staticmethod
    def parse_command_line_configuration(opts):
        return {}

    def get_connection_string(self):
        return ""

class UdpCommunication(_Communication):

    COMMUNICATION_TYPE = "network"

    def __init__(self, transport, messages_file, message_header):
        _Communication.__init__(self, transport, messages_file, message_header)
        self.socket = None
        self.watch = None
        self.connected = False
        self.host = "127.0.0.1"

    def send_message(self, msg, values):
        if self.connected:
            data = self.transport.pack_message_with_values(
                        self.message_header,
                        msg,
                        *values)
            try:
                self.socket.send(data.tostring())
            except socket.error, err:
                print "Could not send: %s" % err

    def on_data_available(self, fd, condition):
        try:
            data = self.socket.recv(1024)
            for header, payload in self.transport.parse_many(data):
                msg = self.messages_file.get_message_by_id(header.msgid)
                if msg:
                    self.emit("message-received", msg, header, payload)
        except socket.error, err:
            print "Could not recv: %s" % err

        return True

    def connect_to_uav(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind((self.host, UDP_PORT))
            self.watch = gobject.io_add_watch(
                            s.fileno(), 
                            gobject.IO_IN | gobject.IO_PRI,
                            self.on_data_available,
                            priority=gobject.PRIORITY_HIGH)
            s.setblocking(0)
            self.socket = s
            self.connected = True
        except socket.error, err:
            print "Couldn't be a udp server on port %d : %s" % (self.PORT, err)

        self.emit("uav-connected", self.is_connected())

    def disconnect_from_uav(self):
        if self.connected:
            gobject.source_remove(self.watch)
            self.socket.close()
            self.connected = False

        self.emit("uav-connected", self.is_connected())

    def is_connected(self):
        return self.connected

    def configure_connection(self, **kwargs):
        pass

    @staticmethod
    def parse_command_line_configuration(opts):
        if len(opts) == 2:
            return {"network_host":opts[0],"network_port":opts[1]}
        return {}

    def get_connection_string(self):
        return "%s:%s" % (self.host, UDP_PORT)

class SerialCommunication(_Communication):

    COMMUNICATION_TYPE = "serial"

    DEFAULT_PORT = "/dev/ttyUSB0"
    DEFAULT_SPEED = "57600"

    def __init__(self, transport, messages_file, message_header):
        _Communication.__init__(self, transport, messages_file, message_header)

        self.serialsender = libserial.SerialSender.SerialSender()
        self.serialsender.connect("serial-connected", self.on_serial_connected)
        #this watch is used to monitor the serial file descriptor for data
        self.watch = None
        #the serial connection details
        self.port = None
        self.speed = None

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
                            priority=gobject.PRIORITY_HIGH
            )

        self.emit("uav-connected", connected)

    def on_serial_data_available(self, fd, condition):
        serial = self.serialsender.get_serial()
        data = serial.read(1)
        for header, payload in self.transport.parse_many(data):
            msg = self.messages_file.get_message_by_id(header.msgid)
            if msg:
                self.emit("message-received", msg, header, payload)
        return True

    def send_message(self, msg, values):
        if msg:
            data = self.transport.pack_message_with_values(
                        self.message_header,
                        msg,
                        *values)
            serial = self.serialsender.get_serial()
            serial.write(data.tostring())

    def connect_to_uav(self):
        self.serialsender.connect_to_port(self.port, self.speed)

    def disconnect_from_uav(self):
        self.serialsender.disconnect_from_port()

    def is_connected(self):
        return self.serialsender.is_open()

    def configure_connection(self, **kwargs):
        self.port = kwargs.get("serial_port")
        self.speed = int(kwargs.get("serial_speed"))

    def get_configuration_default(self):
        return {
            "serial_port":self.DEFAULT_PORT,
            "serial_speed":self.DEFAULT_SPEED
        }

    @staticmethod
    def parse_command_line_configuration(opts):
        if len(opts) == 2:
            return {"serial_port":opts[0],"serial_speed":opts[1]}
        return {}

    def get_connection_string(self):
        return "%s@%s" % (self.port, self.speed)

class DummyCommunication(_Communication):

    COMMUNICATION_TYPE = "test"

    def __init__(self, transport, messages_file, message_header):
        _Communication.__init__(self, transport, messages_file, message_header)
        self._is_open = False
        self.uav_header = wasp.transport.TransportHeaderFooter(acid=wasp.ACID_TEST)
        self.dummy_uav = DummyUAV(messages_file, self.send_message)

    def send_message(self, msg, values):
        #pack the message
        data = self.transport.pack_message_with_values(
                    self.uav_header,
                    msg,
                    *values)

        #then unpack it and re-emit it...
        for header, payload in self.transport.parse_many(data):
            rxmsg = self.messages_file.get_message_by_id(header.msgid)
            self.emit("message-received", rxmsg, header, payload)

        #if this is a command message, also send ACK
        if msg.is_command:
            ackmsg = self.messages_file.get_message_by_name(wasp.fms.COMMAND_ACK)
            payload = ackmsg.pack_values(msg.id)
            self.emit("message-received", ackmsg, self.uav_header, payload)

        #because this function is also used within this class from
        #an idle handler return true to keep getting called
        return True

    def connect_to_uav(self):
        self._is_open = True
        self.emit("uav-connected", self._is_open)

    def disconnect_from_uav(self):
        self._is_open = False
        self.emit("uav-connected", self._is_open)

    def is_connected(self):
        return self._is_open

class FifoCommunication(_Communication):

    COMMUNICATION_TYPE = "fifo"

    def __init__(self, transport, messages_file, message_header):
        _Communication.__init__(self, transport, messages_file, message_header)
        self.readfd = -1
        self.writefd = -1
        self.watch = None
        self.fifo_path = ""

    def send_message(self, msg, values):
        if self.is_connected():
            data = self.transport.pack_message_with_values(
                        self.message_header,
                        msg,
                        *values)
            os.write(self.writefd, data)

    def connect_to_uav(self):
        LOG.info("Connecting to FIFO: %s" % self.fifo_path)

        if self.fifo_path:
            rdpath = self.fifo_path + "_SOGI"
            wrpath = self.fifo_path + "_SIGO"

            if os.path.exists(rdpath) and os.path.exists(wrpath):
                self.readfd = os.open(rdpath, os.O_RDONLY)
                self.writefd = os.open(wrpath, os.O_WRONLY)

            if self.is_connected():
                self.watch = gobject.io_add_watch(
                            self.readfd, 
                            gobject.IO_IN | gobject.IO_PRI,
                            self.on_data_available,
                            priority=gobject.PRIORITY_HIGH)

        self.emit("uav-connected", self.is_connected())

    def on_data_available(self, fd, condition):
        data = os.read(self.readfd, 1)
        for header, payload in self.transport.parse_many(data):
            msg = self.messages_file.get_message_by_id(header.msgid)
            if msg:
                self.emit("message-received", msg, header, payload)
        return True

    def disconnect_from_uav(self):
        if self.is_connected():
            gobject.source_remove(self.watch)
            self.readfd = self.writefd = -1
        self.emit("uav-connected", self.is_connected())

    def is_connected(self):
        return self.writefd != -1 and self.readfd != -1

    def configure_connection(self, **kwargs):
        self.fifo_path = "/tmp/WASP_COMM_TELEMETRY" #kwargs.get("fifo_path")

    def get_connection_string(self):
        return "%s" % self.fifo_path

class DummyUAV:
    """ Generates sensible default messages for a UAV """
    def __init__(self, messages_file, send_message_function, **kwargs):
        """
        kwargs supports multiple disable_XXX arguments to prevent the emission
        of certain classes of message.
            * disable_time
            * disable_comm
            * disable_imu
            * disable_status
            * disable_ppm
            * disable_ahrs
            * disable_gps
        """
        self.messages_file = messages_file
        self.send_message = send_message_function
        self._sendcache = {}

        if not kwargs.get("disable_time"):
            #TIME at 0.1hz
            self._t = 0
            gobject.timeout_add(int(1000/0.1), self._do_time)
        if not kwargs.get("disable_comm"):
            #COMM_STATUS at 0.5hz
            self._generic_send(int(1000/0.5), "COMM_STATUS")
        if not kwargs.get("disable_imu"):
            #IMU at 10hz
            self._generic_send(int(1000/10), "IMU_ACCEL_RAW")
            self._generic_send(int(1000/10), "IMU_MAG_RAW")
            self._generic_send(int(1000/10), "IMU_GYRO_RAW")
        if not kwargs.get("disable_status"):
            #STATUS at 0.5hz
            self._bat = wasp.NoisyWalk(
                                start=145, end=85, delta=-5,
                                value_type=self.messages_file["STATUS"]["vsupply"].pytype)
            self._cpu = wasp.Noisy(
                                value=30, delta=3,
                                value_type=self.messages_file["STATUS"]["cpu_usage"].pytype)
            gobject.timeout_add(int(1000/0.5), self._do_status)
        if not kwargs.get("disable_ppm"):
            #PPM at 10hz
            gobject.timeout_add(int(1000/10), self._do_ppm)
        if not kwargs.get("disable_ahrs"):
            #AHRS at 10hz
            gobject.timeout_add(int(1000/10), self._do_ahrs)
        if not kwargs.get("disable_gps"):
            #GPS at 4 Hz
            gobject.timeout_add(int(1000/4), self._do_gps)
            self._alt = wasp.NoisySine(freq=0.5, value_type=int)
            self._lat = kwargs.get("start_gps_lat", wasp.HOME_LAT)
            self._lon = kwargs.get("start_gps_lon", wasp.HOME_LON)

    def _do_gps(self):
        if random.randint(0,4) == 4:
            self._lat += (random.random()*0.0001)
        if random.randint(0,4) == 4:
            self._lon += (random.random()*0.0001)

        lat = int(self._lat * 1e7)
        lon = int(self._lon * 1e7)
        alt = int(self._alt.value() * 1000.0)

        msg = self.messages_file.get_message_by_name("GPS_LLH")
        self.send_message(msg, (2, 5, lat, lon, alt, 1, 1))
        return True

    def _do_generic_send(self, msgname):
        msg, vals = self._sendcache[msgname]
        self.send_message(msg, vals)
        return True

    def _generic_send(self, freq, msgname):
        msg = self.messages_file.get_message_by_name(msgname)
        if msg:
            self._sendcache[msgname] = (msg, msg.get_default_values())
            gobject.timeout_add(freq, self._do_generic_send, msgname)

    def _do_time(self):
        self._t += 10
        msg = self.messages_file.get_message_by_name("TIME")
        self.send_message(msg, (self._t,))
        return True

    def _do_ahrs(self):
        msg = self.messages_file.get_message_by_name("AHRS_EULER")
        scale = msg.get_field_by_name("imu_phi").coef

        #pitch down by 10 degress, right by 30, heading 0
        phi = 10.0/scale;
        theta = 30.0/scale
        psi = 0.0
        self.send_message(msg, (phi, theta, psi, phi, theta, psi))
        return True

    def _do_ppm(self):
        msg = self.messages_file.get_message_by_name("PPM")
        v = 20000
        n = 100
        self.send_message(msg, (v+random.randint(-n,n), v, v+random.randint(-n,n), v, v+random.randint(-n,n), v))
        return True

    def _do_status(self):
        #   <message name="STATUS" id="8">
        #     <field name="rc" type="uint8" values="OK|LOST|REALLY_LOST"/>
        #     <field name="gps" type="uint8" values="NO_FIX|2D_FIX|3D_FIX"/>
        #     <field name="vsupply" type="uint8" unit="decivolt"/>
        #     <field name="in_flight" type="uint8" values="ON_GROUND|IN_FLIGHT"/>
        #     <field name="motors_on" type="uint8" values="MOTORS_OFF|MOTORS_ON"/>
        #     <field name="autopilot_mode" type="uint8" values="FAILSAFE|KILL|RATE_DIRECT|ATTITUDE_DIRECT|RATE_RC_CLIMB|ATTITUDE_RC_CLIMB|ATTITUDE_CLIMB|RATE_Z_HOLD|ATTITUDE_Z_HOLD|ATTITUDE_HOLD|HOVER_DIRECT|HOVER_CLIMB|HOVER_Z_HOLD|NAV|RC_DIRECT"/>
        #     <field name="cpu_usage" type="uint8" unit="pct"/>
        #   </message>
        msg = self.messages_file.get_message_by_name("STATUS")
        self.send_message(
                msg,(
                msg.get_field_by_name("rc").interpret_value_from_user_string("OK"),
                msg.get_field_by_name("gps").interpret_value_from_user_string("NO_FIX"),
                self._bat.value(),
                msg.get_field_by_name("in_flight").interpret_value_from_user_string("ON_GROUND"),
                msg.get_field_by_name("motors_on").interpret_value_from_user_string("MOTORS_OFF"),
                msg.get_field_by_name("autopilot_mode").interpret_value_from_user_string("FAILSAFE"),
                self._cpu.value()))
        return True

ALL_COMMUNICATION_KLASSES = [
    SerialCommunication,
    DummyCommunication,
    UdpCommunication,
    FifoCommunication
]

def get_source(source_name):
    """
    Parses the source and options as passed on the command line. The user supplies
    the source in the format of 

    name:opt1:opt2

    where opt1 and opt2 meaning depends on the particular source

    :returns: (sournce_name, klass, **options)
    """
    bits = source_name.split(":")
    name = bits[0]
    opts = bits[1:]

    klass = None
    config = {}
    for k in ALL_COMMUNICATION_KLASSES:
        if name == k.COMMUNICATION_TYPE:
            klass = k
            config = k.parse_command_line_configuration(opts)

    if klass == None:
        LOG.warning("Unknown Source: %s" % name)
        klass = DummyCommunication
        name = "test"

    return name,klass,config
