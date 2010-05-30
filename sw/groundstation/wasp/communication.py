import random
import gobject

import libserial.SerialSender

import wasp
import wasp.transport

class Communication(gobject.GObject):

    COMMUNICATION_TYPE = ""

    __gsignals__ = {
        "message-received" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_PYOBJECT,      #message
            gobject.TYPE_PYOBJECT,      #header
            gobject.TYPE_PYOBJECT]),    #payload
        "uav-connected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_BOOLEAN]),     #true if successfully connected to UAV
    }

    def __init__(self, transport, messages_file, *args, **kwargs):
        gobject.GObject.__init__(self)
        self.transport = transport
        self.messages_file = messages_file

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

    def get_connection_string(self):
        return ""

class SerialCommunication(Communication, libserial.SerialSender.SerialSender):

    COMMUNICATION_TYPE = "serial"

    def __init__(self, transport, messages_file):
        Communication.__init__(self, transport, messages_file)
        libserial.SerialSender.SerialSender.__init__(self)
        #this watch is used to monitor the serial file descriptor for data
        self.watch = None
        #the header used when sending a message to the UAV
        self.groundstation_transport_header = wasp.transport.TransportHeaderFooter(acid=0x78)
        #the serial connection details
        self.port = None
        self.speed = None

    def on_serial_connected(self, connected):
        #remove the old watch
        if self.watch:
            gobject.source_remove(self.watch)

        if connected:
            #add new watch
            self.watch = gobject.io_add_watch(
                            self.get_fd(), 
                            gobject.IO_IN | gobject.IO_PRI,
                            self.on_serial_data_available,
                            self.get_serial(),
                            priority=gobject.PRIORITY_HIGH
            )

        self.emit("uav-connected", connected)

    def on_serial_data_available(self, fd, condition, serial):
        data = serial.read(1)
        for header, payload in self.transport.parse_many(data):
            msg = self.messages_file.get_message_by_id(header.msgid)
            if msg:
                self.emit("message-received", msg, header, payload)
        return True

    def send_message(self, msg, values):
        if msg:
            data = self.transport.pack_message_with_values(
                        self.groundstation_transport_header, 
                        msg,
                        *values)
            self.get_serial().write(data.tostring())

    def connect_to_uav(self):
        self.connect_to_port(self.port, self.speed)

    def disconnect_from_uav(self):
        self.disconnect_from_port()

    def is_connected(self):
        return self.is_open()

    def configure_connection(self, **kwargs):
        self.port = kwargs.get("serial_port")
        self.speed = int(kwargs.get("serial_speed"))

    def get_connection_string(self):
        return "%s@%s" % (self.port, self.speed)

class DummySerialCommunication(Communication):

    COMMUNICATION_TYPE = "dummy"

    def __init__(self, transport, messages_file):
        Communication.__init__(self, transport, messages_file)
        self._sendcache = {}
        self._is_open = False
        self.uav_header = wasp.transport.TransportHeaderFooter(acid=0x9A)

        #Write messages to the pipe, so that it is read and processed by
        #the groundstation
        #
        #TIME at 0.1hz
        self._t = 0
        gobject.timeout_add(int(1000/0.1), self._do_time)
        #COMM_STATUS at 0.5hz
        self._generic_send(int(1000/0.5), "COMM_STATUS")
        #IMU at 10hz
        self._generic_send(int(1000/10), "IMU_ACCEL_RAW")
        self._generic_send(int(1000/10), "IMU_MAG_RAW")
        self._generic_send(int(1000/10), "IMU_GYRO_RAW")
        #STATUS at 0.5hz
        self._bat = wasp.NoisyWalk(
                            start=145, end=85, delta=-5,
                            value_type=self.messages_file["STATUS"]["vsupply"].pytype)
        self._cpu = wasp.Noisy(
                            value=30, delta=3,
                            value_type=self.messages_file["STATUS"]["cpu_usage"].pytype)
        gobject.timeout_add(int(1000/0.5), self._do_status)
        #PPM at 10hz
        gobject.timeout_add(int(1000/10), self._do_ppm)
        #AHRS at 10hz
        gobject.timeout_add(int(1000/10), self._do_ahrs)
        #GPS at 4 Hz
        gobject.timeout_add(int(1000/4), self._do_gps)
        self._alt = wasp.NoisySine(freq=0.5, value_type=int)
        self._lat = -43.520451
        self._lon = 172.582377

    def _do_gps(self):
        if random.randint(0,4) == 4:
            self._lat += (random.random()*0.0001)
        if random.randint(0,4) == 4:
            self._lon += (random.random()*0.0001)

        lat = int(self._lat * 1e7)
        lon = int(self._lon * 1e7)
        alt = self._alt.value() * 1000.0

        msg = self.messages_file.get_message_by_name("GPS_LLH")
        return self._send(msg, 2, 5, lat, lon, alt, 1, 1)

    def _do_generic_send(self, msgname):
        msg, vals = self._sendcache[msgname]
        self._send(msg, *vals)
        return True

    def _generic_send(self, freq, msgname):
        msg = self.messages_file.get_message_by_name(msgname)
        if msg:
            self._sendcache[msgname] = (msg, msg.get_default_values())
            gobject.timeout_add(freq, self._do_generic_send, msgname)

    def _send(self, msg, *vals):
        self.send_message(msg, vals)
        return True

    def _do_time(self):
        self._t += 10
        msg = self.messages_file.get_message_by_name("TIME")
        return self._send(msg, self._t)

    def _do_ahrs(self):
        msg = self.messages_file.get_message_by_name("AHRS_EULER")
        scale = msg.get_field_by_name("imu_phi").coef

        #pitch down by 10 degress, right by 30, heading 0
        phi = 10.0/scale;
        theta = 30.0/scale
        psi = 0.0
        return self._send(msg, phi, theta, psi, phi, theta, psi)

    def _do_ppm(self):
        msg = self.messages_file.get_message_by_name("PPM")
        v = 20000
        n = 100
        return self._send(msg, v+random.randint(-n,n), v, v+random.randint(-n,n), v, v+random.randint(-n,n), v)

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
        return self._send(
                msg,
                msg.get_field_by_name("rc").interpret_value_from_user_string("OK"),
                msg.get_field_by_name("gps").interpret_value_from_user_string("NO_FIX"),
                self._bat.value(),
                msg.get_field_by_name("in_flight").interpret_value_from_user_string("ON_GROUND"),
                msg.get_field_by_name("motors_on").interpret_value_from_user_string("MOTORS_OFF"),
                msg.get_field_by_name("autopilot_mode").interpret_value_from_user_string("FAILSAFE"),
                self._cpu.value())

    def send_message(self, msg, values):
        #pack the message
        data = self.transport.pack_message_with_values(
                    self.uav_header, 
                    msg,
                    *values)

        #then unpack it and re-emit it...
        for header, payload in self.transport.parse_many(data):
            msg = self.messages_file.get_message_by_id(header.msgid)
            self.emit("message-received", msg, header, payload)

    def connect_to_uav(self):
        self._is_open = True
        self.emit("uav-connected", self._is_open)

    def disconnect_from_uav(self):
        self._is_open = False
        self.emit("uav-connected", self._is_open)

    def is_connected(self):
        return self._is_open

