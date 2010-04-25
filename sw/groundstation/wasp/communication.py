import random
import os
import gobject
import serial

import libserial.SerialSender

import wasp
import wasp.transport

class SerialCommunication(libserial.SerialSender.SerialSender):
    """
    Reads data from the serial port 
    """
    def read(self, nbytes=5):
        if self.is_open():
            try:
                return self._serial.read(nbytes)
            except  serial.SerialTimeoutException:
                pass
        return ""
    
    def write(self, data):
        if self.is_open():
            self._serial.write(data)

class DummySerialCommunication(gobject.GObject):
    """
    For testing groundstation with no UAV
    """

    __gsignals__ = {
        "serial-connected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [
            gobject.TYPE_BOOLEAN]),     #True if successfully connected to the port
        }

    def __init__(self, messages, transport, acid):
        gobject.GObject.__init__(self)
        self._readfd, self._writefd = os.pipe()

        self._messages = messages        
        self._transport = transport
        self._header = wasp.transport.TransportHeaderFooter(acid=acid)

        self._sendcache = {}
        self._is_open = False

        #Write messages to the pipe, so that it is read and processed by
        #the groundstation
        #
        #TIME at 1hz
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
                            value_type=self._messages["STATUS"]["vsupply"].pytype)
        self._cpu = wasp.Noisy(
                            value=30, delta=3,
                            value_type=self._messages["STATUS"]["cpu_usage"].pytype)
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

        msg = self._messages.get_message_by_name("GPS_LLH")
        return self._send(msg, 2, 5, lat, lon, alt, 1, 1)

    def _do_generic_send(self, msgname):
        msg, vals = self._sendcache[msgname]
        self._send(msg, *vals)
        return True

    def _generic_send(self, freq, msgname):
        msg = self._messages.get_message_by_name(msgname)
        if msg:
            self._sendcache[msgname] = (msg, msg.get_default_values())
            gobject.timeout_add(freq, self._do_generic_send, msgname)

    def _send(self, msg, *vals):
        data = self._transport.pack_message_with_values(
                        self._header,
                        msg,
                        *vals)
        os.write(self._writefd, data.tostring())
        return True

    def _do_time(self):
        self._t += 10
        msg = self._messages.get_message_by_name("TIME")
        return self._send(msg, self._t)

    def _do_ahrs(self):
        msg = self._messages.get_message_by_name("AHRS_EULER")
        scale = msg.get_field_by_name("imu_phi").coef

        #pitch down by 10 degress, right by 30, heading 0
        phi = 10.0/scale;
        theta = 30.0/scale
        psi = 0.0
        return self._send(msg, phi, theta, psi, phi, theta, psi)

    def _do_ppm(self):
        msg = self._messages.get_message_by_name("PPM")
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
        msg = self._messages.get_message_by_name("STATUS")
        return self._send(
                msg,
                msg.get_field_by_name("rc").interpret_value_from_user_string("OK"),
                msg.get_field_by_name("gps").interpret_value_from_user_string("NO_FIX"),
                self._bat.value(),
                msg.get_field_by_name("in_flight").interpret_value_from_user_string("ON_GROUND"),
                msg.get_field_by_name("motors_on").interpret_value_from_user_string("MOTORS_OFF"),
                msg.get_field_by_name("autopilot_mode").interpret_value_from_user_string("FAILSAFE"),
                self._cpu.value())

    def get_fd(self):
        return self._readfd

    def connect_to_port(self):
        self.emit("serial-connected", True)
        self._is_open = True
        return True

    def disconnect_from_port(self):
        self.emit("serial-connected", False)
        self._is_open = False

    def is_open(self):
        return self._is_open

    def write(self, data):
        os.write(self._writefd, data)

    def read(self, nbytes=5):
        return os.read(self._readfd, nbytes)




